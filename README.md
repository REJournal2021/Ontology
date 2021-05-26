# Ontology

## Introduction

To regenerate our results for Scene Graph Generation you should have do follow our guideline:

1. Run unbiased Scene graph generation on your dataset to generate descriptions for your images.
2. Filter the results and export them to the sqlite database.
3. Augment the dataset based on previous results.


### Unbiased Scene Graph Generation

We have used this [repository](https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch) to generate scene graphs, please follow their instructions to install the scene graph benchmark.

After installing USGG based on their manual you can run it for any dataset you want. There is an example of how to run it for the COOC downsample in this [file](https://github.com/asecnf2021/MLClassifiers/blob/main/coco_usgg.ipynb), you can use it to run the USGG.

Then you need to filter the result of the previous step. To do that just keep the top 30 objects and top 20 relations in each image. Furthermore, because sometimes we need to focus only on the pedestrian, we generated other results for the pedestrian, keeping the top 20 relations which at least one of its objects is the pedestrian label. So, we have two separate databases which store the results([top.db](https://drive.google.com/file/d/1xIU5-z87P6Npvmjp-i933VyVCDzU8wGr/view?usp=sharing) and, [person.db](https://drive.google.com/file/d/1U01WgpqBUWi2l-z2G8Y0fu9h3WPjnQOn/view?usp=sharing)). The databases are in form of SQLITE. Also, if you like you can export the databases to the Pandas data frame. 
