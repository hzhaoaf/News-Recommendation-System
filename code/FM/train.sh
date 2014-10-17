#设置常量
path="/Volumes/BigData/Developer/News-Recommendation-System/data/FM/"
train_data="${path}train.libfm"
test_data="${path}test.libfm"
cd libfm-1.42.src/bin/

#开始训练
out_file="result.txt"
./libFM -task r -train $train_data -test $test_data -dim '1,1,8' -out $out_file
