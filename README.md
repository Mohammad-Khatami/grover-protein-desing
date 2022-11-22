# grover-protein-desing
you should have qiskit V 0.24.0 to run this code. to install a specific version of qiskit, this youtube link would be helpful:https://www.youtube.com/watch?v=L1TPD43UTZM 
the code is tested with python 3.8.2 version.
the expected run time and the resources required are provided in the supplemntary data of the paper.

# For the SP model:
In the "codes" folder under the "SP-model", you can find codes for different circuits used in this study, employing SP-model algorithm.
The file name "functions_ripple_carry_adder_E8.py" file has the necessary functions used in the SP models.
The python codes are named in a way that represent the conditions used for the circuits. For example "2res-1inter-m4-iter-1-E2.py" file is for the circuit with two designable sties (2res), 1 interactions (1inter), m=4, R=1 (iter-1) and E_threshol=2 (E2). One can easily change the value in the file to see their effects.
File name "SP-3res-2inter-m5-iter-1-E7.txt" contains an expected set of ouputs for the code "3res-2inter-m5-iter-1-E7.py".


# For the MR model:
In the "codes" folder under the "MR-model", you can find codes for different circuits used in this study, employing MR-model algorithm.
The file name "func_apr_20_2021_decim_E_dec.py" file has the necessary functions used in the MR models.
The python codes are named in a way that represent the conditions used for the circuits. For example "3r_3c_4i5d_r1_e.70.py" file is for the circuit with three designable sties (3r), 3 interactions (3c), m=9 with 4 qubits for integer part and 5 to show decimal values (4i5d) , r=1 (r1) and E_threshol=70% of minumum energy (e.70). One can easily change the value in the file to see their effects.
File name "MR_s3_i3_m9p5_R1_Eth80.txt" contains an expected set of ouputs for the code "3r_3c_4i5d_r1_e.80.py". 
