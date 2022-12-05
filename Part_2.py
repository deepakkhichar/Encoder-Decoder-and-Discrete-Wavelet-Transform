import cv2
import pywt
import numpy as np
import copy
img=cv2.imread("sample_image.png",0)
img=np.asarray(img)
print(img.shape)
# img[img>150]=0
# cv2.imshow("Original Image",img)
# cv2.waitKey(0)

def prune(dummy,threshold_pow):
    print("    Energy of one of the sub-band is",np.sqrt(np.mean(np.multiply(dummy, dummy))))
    threshold=(np.mean(abs(dummy)))/pow(2,threshold_pow)
    dummy[dummy>threshold]=0
    return dummy

print("\n------------- Using different threshold values and different level of decompositions ---------------\n\n")
possible_level_of_decomposition=[3,4]
possible_threshold_pow=[1,16]
for level_of_decomposition in possible_level_of_decomposition:
    for threshold_pow in possible_threshold_pow:
        print("\nFor Levels of decomposition =",level_of_decomposition," and threshold = average /",threshold_pow,":")
        dummy=copy.deepcopy(img)
        coeffs=pywt.wavedec2(dummy,'db5', mode='periodization',level=level_of_decomposition)
        
        coeffs[0] = prune(coeffs[0], threshold_pow)
        for level in range(level_of_decomposition):
            coeffs[level + 1] = [prune(d, threshold_pow) for d in coeffs[level + 1]]
        img_recovered = pywt.waverec2(coeffs, 'db5', mode='periodization')
        cv2.imshow("Original Image",img)
        cv2.imshow("Recoverd image with threshold = average/"+str(threshold_pow)+" and level of decomposition = "+str(level_of_decomposition),img_recovered) 
        cv2.waitKey(0)


print("\n\n\n------------- varying the number of coefficients retained ---------------\n\n")
possible_level_of_decomposition=[3,4]
possible_percentage_coefficients_that_can_be_discarded = ["50 %","95 %","99.5 %"]

for level_of_decomposition in possible_level_of_decomposition:
    for percentage_coefficients_that_can_be_discarded in possible_percentage_coefficients_that_can_be_discarded:
        print("\nLevels of decomposition =",level_of_decomposition," and",percentage_coefficients_that_can_be_discarded," coefficients discarded :")
        percent=float(percentage_coefficients_that_can_be_discarded[:-2])/100
        dummy=copy.deepcopy(img)
        coeffs=pywt.wavedec2(dummy,'db5',level=level_of_decomposition, mode='periodization')
        arr, slices = pywt.coeffs_to_array(coeffs)
        arr_sorted = np.sort(np.abs(arr.reshape(-1)))
        threshold = arr_sorted[int(np.floor(percent*len(arr_sorted)))]
        arr[arr>threshold]=0
        
        coeffs_filtered = pywt.array_to_coeffs(arr,slices,output_format='wavedec2')
        
        img_recovered  = pywt.waverec2(coeffs_filtered,'db5', mode='periodization')
        cv2.imshow("Original Image",img)
        cv2.imshow("Recoverd image with "+percentage_coefficients_that_can_be_discarded+" coefficients discarded and level of decomposition = "+str(level_of_decomposition),img_recovered) 
        cv2.waitKey(0)
cv2.destroyAllWindows()