#!/bin/sh

#echo cleaning pipes
#
#echo Cleaning | tee fp_ser_eng | tee fp_eng_ser
#
#exec 3>fp_ser_eng
#cat fp_ser_eng & exec 3>&-
#
#exec 3>fp_eng_ser
#cat fp_eng_ser & exec 3>&-

echo starting server and client
 
./server_exec & ./dvizh_ok_exec
