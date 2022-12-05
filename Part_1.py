import random
import copy
import math

def convert_string_to_binary(s):
    binary_string=""
    for i in s:
        # Taking ASCII value of each char in string s
        ascii_val = ord(i)
        # Convert ASCII value to binary
        binary_val = bin(ascii_val)
        l=len(str(binary_val))
        if l<9:
            dummy=""
            while(l!=9):
                dummy=dummy+"0"
                l+=1
            binary_string=binary_string+dummy+binary_val[2:]
            continue
        binary_string=binary_string+binary_val[2:]
    return (binary_string)

def convert_binary_to_string(binary_string):
    l=len(binary_string)
    original_string=""
    i=0
    while i<l:
        s=int(binary_string[i:i+7],2)
        original_string=original_string+chr(s)
        i+=7
    return original_string

def encoding_binary_string_using_huffman(s):
    number_of_zeros=0
    number_of_ones=0
    for i in s:
        if i=='0':
            number_of_zeros+=1
        else:
            number_of_ones+=1
    probability_of_zero=float(number_of_zeros)/(number_of_zeros+number_of_ones)
    probability_of_one=1-probability_of_zero
    encoded_s=""
    for i in s:
        if i=='0':
            encoded_s=encoded_s+"0"
        elif i=='1':
            encoded_s=encoded_s+"1"
    return encoded_s

# For Extended Huffman
class node:
	def __init__(self, freq, symbol, left=None, right=None):
		# frequency of symbol
		self.freq = freq

		# symbol name (character)
		self.symbol = symbol

		# node left of current node
		self.left = left

		# node right of current node
		self.right = right

		# tree direction (0/1)
		self.huff = ''

#For Extended Huffman 
def encoded_value_of_Node(dic,node, val=''):
    newVal = val + str(node.huff)
  
    if(node.left):
        encoded_value_of_Node(dic,node.left, newVal)
    if(node.right):
        encoded_value_of_Node(dic,node.right, newVal)
    if(not node.left and not node.right):
        dic[node.symbol]=newVal
  

def encoding_binary_string_using_extended_huffman(s,n=4):
    # characters for huffman tree
    chars=[]
    for i in range(int(pow(2,n))):
        binary_val = bin(i)
        binary_string=str(binary_val)[2:]
        l=len(binary_string)
        if l<n:
            dummy=""
            while(l!=n):
                dummy=dummy+"0"
                l+=1
            binary_string=dummy+binary_string
        chars.append(binary_string)
    chars.sort()
    # frequency of characters
    freq = [0 for i in range(int(pow(2,n)))]
    for i in range(0, len(s), n):
        index=int(s[i:i+n],2)
        freq[index]+=1
    
    # list containing unused nodes
    nodes = []
    
    # converting characters and frequencies into huffman tree nodes
    for x in range(len(chars)):
    	nodes.append(node(freq[x], chars[x]))
        
    while len(nodes) > 1:
    	nodes = sorted(nodes, key=lambda x: x.freq)
    	left = nodes[0]
    	right = nodes[1]
    
    	left.huff = 0
    	right.huff = 1
    
    	newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)
    
    	nodes.remove(left)
    	nodes.remove(right)
    	nodes.append(newNode)
    dic={}
    encoded_value_of_Node(dic,nodes[0])
    encoded=""
    for i in range(0, len(s), n):
        if i+4>=len(s):
            encoded=encoded+s[i:]
            break
        encoded=encoded+dic[s[i:i+n]]
    return encoded

def ar_code(n,precision):
    s=""
    while(len(s)<precision):
        n=n*2
        s=s+str(int(n))
        if n>=1:
            n=n-1
    return s


def encoding_binary_string_using_arithmatic(s,n=4):
    chars=[]
    for i in range(int(pow(2,n))):
        binary_val = bin(i)
        binary_string=str(binary_val)[2:]
        l=len(binary_string)
        if l<n:
            dummy=""
            while(l!=n):
                dummy=dummy+"0"
                l+=1
            binary_string=dummy+binary_string
        chars.append(binary_string)
    chars.sort()
    # frequency of characters
    freq = [0 for i in range(int(pow(2,n)))]
    total_freq=0
    for i in range(0, len(s), n):
        index=int(s[i:i+n],2)
        freq[index]+=1
        total_freq+=1
    prob = [float(freq[i])/total_freq for i in range(len(freq))]
    num=0
    cum_prob=[]
    for i in range(len(prob)):
        num+=prob[i]
        cum_prob.append(num)
    tx=[]
    fx_previous=0
    for i in range(len(prob)):
        tx.append(fx_previous+prob[i]/2)
        fx_previous=cum_prob[i]
    
    
    log_plus_1=[]
    for i in range(len(prob)):
        if prob[i]==0:
            log_plus_1.append(-1)
            continue
        log_plus_1.append(int(-math.log(prob[i],2)+1))
    
    dec={}
    
    for i in range(len(chars)):
        dec[chars[i]]=ar_code(tx[i],log_plus_1[i])
    
    encoded=""
    for i in range(0, len(s), n):
        if i+4>=len(s):
            encoded=encoded+s[i:]
            break
        encoded=encoded+dec[s[i:i+n]]
    return encoded
    

def encode(s,method):
    if method=="(1) Huffman":
        return encoding_binary_string_using_huffman(s)        
    elif method=="(2) Extended Huffman":
        return encoding_binary_string_using_extended_huffman(s,4)
    else:
        return encoding_binary_string_using_arithmatic(s,5)
    
    
    
    




#Reading the text file and converting to binary string
file=open("sample_text.txt","r")
original_data=file.read()
# print(original_data)
binary_data=convert_string_to_binary(original_data)
l=len(binary_data)


# ------------------------------------------------Experiment 1---------------------------------------------------------------------   

print("\n\n-------------------------------------Part 1 Experiment 1-------------------------------------------------\n")


choices_of_d=[10,100,200,500,5000]
for d in choices_of_d:
    if l<d:
        print("Cannot complete the task at d =",d," since maximum allowed possible value of d is",l)
        continue
    index_of_1=random.sample(range(l), d)
    random_binary_error_pattern="0"*l
    for i in index_of_1:
        random_binary_error_pattern=random_binary_error_pattern[:i]+"1"+random_binary_error_pattern[i+1:]
    # print(random_binary_error_pattern)
    
    y=copy.deepcopy(binary_data)
    for i in index_of_1:
        if y[i]=='0':
            y=y[:i]+"1"+y[i+1:]
        else:
            y=y[:i]+"0"+y[i+1:]
    
    decoded_y=convert_binary_to_string(y)
    
    num_total_characters=len(original_data)
    num_modified_characters=0
    for i in range(num_total_characters):
        if original_data[i]!=decoded_y[i]:
            num_modified_characters+=1
    # print(num_modified_characters)
    # print(num_total_characters)
    print("When d =",d,"percentage of modified characters with respect to the input file is",float(num_modified_characters)/num_total_characters*100,"%")
    
# ------------------------------------------------Experiment 2------------------------------------------------------------------------    

print("\n\n\n\n------------------------------------- Part 1 Experiment 2-------------------------------------------------\n")
k=100
chunks = [binary_data[i:i+k] for i in range(0, len(binary_data), k)]
print("using k =",k)
choices_of_d=[10,100,200,500,5000]
encoding_methods=["(1) Huffman","(2) Extended Huffman","(3) Arithmatic"]
for d in choices_of_d:
    print("\n\nWhen d =",d,":")
    for encoding_method in encoding_methods:
        encoded_chunks=[]
        for chunk in chunks:
            encoded_chunks.append(encode(chunk,encoding_method))
        encoded_binary_data=''.join(encoded_chunks)
        
        l=len(encoded_binary_data)
        if l<d:
            print("    For",encoding_method,"Encoding Method; Cannot complete the task at d =",d," since maximum allowed possible value of d is",l)
            continue
        index_of_1=random.sample(range(l), d)
        random_binary_error_pattern="0"*l
        for i in index_of_1:
            random_binary_error_pattern=random_binary_error_pattern[:i]+"1"+random_binary_error_pattern[i+1:]
        # print(random_binary_error_pattern)
        
        y=copy.deepcopy(encoded_binary_data)
        for i in index_of_1:
            if y[i]=='0':
                y=y[:i]+"1"+y[i+1:]
            else:
                y=y[:i]+"0"+y[i+1:]
        if encoding_method=="(1) Huffman":
            decoded_y=convert_binary_to_string(y)
            
            num_total_characters=len(original_data)
            num_modified_characters=0
            for i in range(num_total_characters):
                if original_data[i]!=decoded_y[i]:
                    num_modified_characters+=1
            # print(num_modified_characters)
            # print(num_total_characters)
            print("    Using",encoding_method,"as encoding method;","percentage of modified characters with respect to the input file is",float(num_modified_characters)/num_total_characters*100,"%")
        else:
            print("    Length of binary string before and after applying",encoding_method,"encoding method is",len(binary_data),",",len(encoded_binary_data),"respectively, i.e.,",100-float(len(encoded_binary_data))/len(binary_data)*100,"% compression")






















