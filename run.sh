#!/bin/sh

# ================= INPUT =================
WORKDIR=$1
SRCDIR=$2

if [ -z "$WORKDIR" ] || [ -z "$SRCDIR" ]; then
  echo "Usage: run.sh <workdir> <srcdir>"
  exit 1
fi

# ================= SETUP =================
mkdir -p "$WORKDIR"
cd "$WORKDIR" || exit 1

rm -f dbg.*.log

# ================= PREPARE GRADER =================
mkdir grade-dir
cd grade-dir || exit 1

wget https://spark-public.s3.amazonaws.com/cloudcomputing2/assignments/mp2_assignment.zip || { echo 'ERROR wget'; exit 1; }

unzip mp2_assignment.zip || { echo 'ERROR unzip'; exit 1; }

cd mp2_assignment || exit 1

# ================= COPY YOUR CODE =================
cp "$SRCDIR"/MP2Node.* . || { echo 'Missing MP2Node files'; exit 1; }
cp "$SRCDIR"/MP1Node.* . || { echo 'Missing MP1Node files'; exit 1; }

# ================= BUILD =================
make clean > /dev/null 2>&1
make > /dev/null 2>&1 || { echo 'Build failed'; exit 1; }

# ================= RUN TESTS =================

echo "CREATE test"
./Application testcases/create.conf
cp dbg.log "$WORKDIR/dbg.0.log"

echo "DELETE test"
./Application testcases/delete.conf
cp dbg.log "$WORKDIR/dbg.1.log"

echo "READ test"
./Application testcases/read.conf
cp dbg.log "$WORKDIR/dbg.2.log"

echo "UPDATE test"
./Application testcases/update.conf
cp dbg.log "$WORKDIR/dbg.3.log"

# ================= CLEANUP =================
cd "$WORKDIR" || exit 1
rm -rf grade-dir