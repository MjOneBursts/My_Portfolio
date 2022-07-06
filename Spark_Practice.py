# Databricks notebook source
#Michael Jara
#Short Data
sc = spark.sparkContext
text = sc.textFile("FileStore/tables/lab3short")
words = text.map(lambda line: line.split(" ")).persist()
words.collect()

wordTuples = words.map(lambda word: (word[0], sorted(word[1:])))
reduced = wordTuples.sortByKey()
print(reduced.collect())

# COMMAND ----------

#Full Data
sc = spark.sparkContext
text = sc.textFile("FileStore/tables/lab3full")
words = text.map(lambda line: line.split(" ")).persist()
words.collect()

wordTuples = words.map(lambda word: (word[0], sorted(word[1:])))
reduced = wordTuples.sortByKey()
print("count: ", reduced.count())
print(reduced.take(10))
