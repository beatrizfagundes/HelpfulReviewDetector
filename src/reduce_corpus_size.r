
set.seed(2)

# corpus_Amazon <- read.csv('AmazonReviews_DigitalMusic_filtered.csv',
#                           header=TRUE, sep=',')



# corpus_Amazon_helpful <- corpus_Amazon[ sample( which(corpus_Amazon$Class=='helpful'), 4632), ]
# print(nrow(corpus_Amazon_helpful))
# print(ncol(corpus_Amazon_helpful))

# corpus_Amazon_not_helpful <- corpus_Amazon[ sample( which(corpus_Amazon$Class=='not_helpful'), 4632), ]
# print(nrow(corpus_Amazon_not_helpful))
# print(ncol(corpus_Amazon_not_helpful))

# corpus_Amazon <- rbind(corpus_Amazon_helpful, corpus_Amazon_not_helpful)
# print(nrow(corpus_Amazon))
# print(ncol(corpus_Amazon))

# write.csv(corpus_Amazon, 'AmazonReviews_DigitalMusic_balanced.csv', row.names=FALSE)

# corpus_Cellphones <- read.csv('AmazonReviews_CellPhones.csv', header=TRUE, sep=',')

# # print(summary(corpus_Cellphones$Class))
# corpus_Cellphones_helpful <- corpus_Cellphones[ sample( which(corpus_Cellphones$Class=='helpful'), 900), ]
# print(nrow(corpus_Cellphones_helpful))
# print(ncol(corpus_Cellphones_helpful))

# corpus_Cellphones_not_helpful <- corpus_Cellphones[ sample( which(corpus_Cellphones$Class=='not_helpful'), 900), ]
# print(nrow(corpus_Cellphones_not_helpful))
# print(ncol(corpus_Cellphones_not_helpful))

# corpus_Cellphones <- rbind(corpus_Cellphones_helpful, corpus_Cellphones_not_helpful)
# print(nrow(corpus_Cellphones))
# print(ncol(corpus_Cellphones))

# write.csv(corpus_Cellphones, 'Cellphones_balanced.csv', row.names=FALSE)

corpus_Sports <- read.csv('Sports.csv', header=TRUE, sep=',')

# print(summary(corpus_Sports$Class))
corpus_Sports_helpful <- corpus_Sports[ sample( which(corpus_Sports$Class=='helpful'), 2752), ]
print(nrow(corpus_Sports_helpful))
print(ncol(corpus_Sports_helpful))

corpus_Sports_not_helpful <- corpus_Sports[ sample( which(corpus_Sports$Class=='not_helpful'), 2752), ]
print(nrow(corpus_Sports_not_helpful))
print(ncol(corpus_Sports_not_helpful))

corpus_Sports <- rbind(corpus_Sports_helpful, corpus_Sports_not_helpful)
print(nrow(corpus_Sports))
print(ncol(corpus_Sports))

write.csv(corpus_Sports, 'Sports_balanced.csv', row.names=FALSE)


# corpus_Canada <- read.csv('/Users/beatrizfagundes/IC/Reuniao17-06--07/csv-collections/BEFORE-preprocessing/Canada-Highlights-2011-2012_full.csv',
#                           header=TRUE, sep=',')

# # print(table(corpus_Canada$Class == 'cfb'))

# corpus_Canada_helpful <- corpus_Canada[ sample( which(corpus_Canada$Class=='cfb'), 1299), ]
# print(nrow(corpus_Canada_helpful))
# print(ncol(corpus_Canada_helpful))

# corpus_Canada_not_helpful <- corpus_Canada[ sample( which(corpus_Canada$Class=='noncfb'), 1299), ]
# print(nrow(corpus_Canada_not_helpful))
# print(ncol(corpus_Canada_not_helpful))

# corpus_Canada <- rbind(corpus_Canada_helpful, corpus_Canada_not_helpful)
# print(nrow(corpus_Canada))
# print(ncol(corpus_Canada))

# write.csv(corpus_Canada, 'Canada_balanced.csv', row.names=FALSE)

