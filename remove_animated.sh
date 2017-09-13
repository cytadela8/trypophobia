PATH=$1

shopt -s globstar
for i in $PATH/**/*.gif; do
  if [ `identify "$i" | wc -l` -gt 1 ] ; then
    echo move "$i"
  else
    echo dont move "$i"
  fi
done
