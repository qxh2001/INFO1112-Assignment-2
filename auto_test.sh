cd tests
VAR=$(find . -name "*.sh")
for files in $VAR;
do
  echo File name: "$files"
  bash "$files"
done