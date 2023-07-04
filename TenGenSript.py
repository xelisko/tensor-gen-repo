#!/usr/bin/env python3

import argparse
import numpy as np

def main():

  # Read the parameters from input
  parser = argparse.ArgumentParser(description='Define the tensor data')

  # Binary representation format
  parser.add_argument('bin_repres', type=int, help = '1 - fixed point \n 2 - floating point \n 3- posit \n' )

  # n-D vector
  parser.add_argument('Tshape_in', type=str, help = 'exact size of eaach tensor dimension')

  # bits per word
  parser.add_argument('bin_size', type=int, help = 'size of the binary words in bits')


  args = parser.parse_args()
  # sanity check0
  print (args.bin_repres)
  print (args.Tshape_in)
  print (args.bin_size)
  #print (sum_function(2,3))



  # MAIN
  # generation of the tensor values
  Z = generate_tensor_values(args.Tshape_in)

  # take n-D tensor, convert it to 1D tensor
  print ("check tensor shape:", str(Z.shape))
  Z = Z.reshape((-1))#(2,90)
  print ('check tensoe 1d shape:', str(len(Z)))
  print (Z)
  # print out the binary values
  if (args.bin_repres == 1):
     for number in Z:
       b = float_to_Fixed(number, args.bin_size)
       print (b)

  elif (args.bin_repres == 2):
     for number in Z:
       b = Floating_point(number, args.bin_size)
       print (b)

  elif (args.bin_repres == 3):
     print ("not finished yet")
    # Posit()

  return

# generates random values (keeping the same over multiple running of the
# function) for a custom shape tensor from the input
def generate_tensor_values(shape_str):
    shape = tuple(int(i) for i in shape_str.split(", "))
    np.random.seed(13)
    data = np.random.normal(0,1,shape)
    return data


# sanity check sum function
def sum_function(a,b):
  return a+b

# ------------------  FIXED POINT ------------------

def float_to_Fixed(number, bin_size, places = 30):

     # Splitting float into whole and decimal parts for conversion
     whole, dec = str(number).split(".") ## try convert to int here
     whole = int(whole)
     dec = int(dec)

     # Convert the whole part
     res = bin(whole).lstrip("-0b").strip("0b")# + "."

     # Convert the decimal part
     for i in range (places):
       whole, dec = str((decimal_converter(dec)* 2)).split(".")
       dec = int(dec)
       res += whole

     # Make all n bits
     res = res.zfill(bin_size)

     # applying 2's complement
     if (number < 0):

        # invert all the bits
        res_neg = ""
        for i in range (bin_size):
            if (res[i] == "0"):
                res_neg += "1"
            else:
                res_neg += "0"
        # add 1 to LSB
        res_neg = add_binary(res_neg, "1")
        return res_neg

     return res

def decimal_converter(num):
    while num > 1:
        num /= 10
    return float(num)

def add_binary(x,y):
    maxlen = max( len(x), len(y) )

    # Normalize lengths
    x = x.zfill( maxlen )
    y = y.zfill( maxlen )

    result = ''
    carry = 0

    for i in range( maxlen-1, -1, -1 ):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0

        # r can be 0,1,2,3 (carry + x[i] + y[i])
        # and among these, for r==1 and r==3 you will have result bit = 1
        # for r==2 and r==3 you will have carry = 1

        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry != 0 : result = '1' + result

    return result.zfill(maxlen)


# ------------------------ FLOATING POINT ---------------------------
def Floating_point(number, bin_size):
  places = 23 # as the mantissa is 23 bits
  # sign bit
  if (number < 0):
    sign_bit = 1
  else:
    sign_bit = 0

  number = abs(number)

  # convert to fixed point 1'c - splitting float into whole and decimal parts for conversion
  whole, dec = str(number).split(".") ## try convert to int here
  whole = int(whole)
  dec = int(dec)

  # Convert the whole part
  res = bin(whole).lstrip("-0b").strip("0b")# + "."

  # Calculate the Exponent
  exponent = len(str(res)) - 1 + 127 #for bias offset
  exponent = bin(exponent).lstrip("-0b").zfill(8) # converts to 8-bit binary

  # Convert the decimal part
  for i in range (places):
    whole, dec = str((decimal_converter(dec) * 2)).split(".")
    dec = int(dec)
    res += whole

  # cOMPIling the components together
  result = str(sign_bit)+"_"+str(exponent)+"_"+str(res[1:-1])
#    print ("floating point", result)
  result = result.ljust(34, '0')
 #   print (result)
  return result


#------------------------- POSIT ----------------------------








if __name__ == "__main__":
  main()
