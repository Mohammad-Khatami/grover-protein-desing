# grover-protein-desing
you should have qiskit V 0.24.0 to run this code. to install a specific version of qiskit, this youtube link would be helpful:https://www.youtube.com/watch?v=L1TPD43UTZM 
the code is tested with python 3.8.2 version.
the expected run time and the resources required are provided in the supplemntary data of the paper.

# For the SP model:
the file name "functions_ripple_carry_adder_E8.py" file has the necessary functions used in the SP models.
the file name SP-3res-2inter-m5-iter-1-E7.py contains the algorithm in the SP model with s=3,i=2,Eth=-7 with iteration of R=1 and m=5. one can easily change the value in the file to see their effects.
File name "SP-3res-2inter-m5-iter-1-E7.txt" contains an expected set of ouputs for the code.


# For the MR model:
the file name "func_apr_20_2021_decim_E_dec.py" file has the necessary functions used in the MR models.
the file name MR_s3_ie_m9p5_R1_Eth80.py contains the algorithm in the MR model with s=3,i=3,Eth=80% of E_max with iteration of R=1 and m=9 (p=5). one can easily change the value in the file to see their effects.
File name "MR_s3_i3_m9p5_R1_Eth80.txt" contains an expected set of ouputs for the code.
