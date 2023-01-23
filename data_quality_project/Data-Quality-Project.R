dataset="/Users/user/Desktop/text-mining/VariableCibles.csv"

path_to_save_data='/Users/user/Desktop/'

library(httr)

url <- "http://127.0.0.1:8000/api/correction"
result_correction = content(POST(url,body = list(file = dataset,target="profession")))

#result to dataframe
new_data <- as.data.frame(do.call(cbind, result_correction$file))
#change list class to character in the dataframe
new_data$profession <- unlist(new_data$profession, use.names = FALSE)
new_data$Corrected <- unlist(new_data$Corrected, use.names = FALSE)

#save dataframe as csv
write.csv(new_data, paste(path_to_save_data,"corrected.csv",sep=","), row.names=FALSE)


url2 <- "http://127.0.0.1:8000/api/categorization"
list_professions <- paste("ménagère","enseignement")
result_categorization = content(POST(url2, body = list(file = "/Users/user/Desktop/corrected.csv",target="profession",elements=list_professions)))

new_data2 <- as.data.frame(do.call(cbind, result_categorization$corrected_dataset))
new_data2$profession <- unlist(new_data2$profession, use.names = FALSE)
new_data2$Corrected <- unlist(new_data2$Corrected, use.names = FALSE)
new_data2$Categorie <- unlist(new_data2$Categorie, use.names = FALSE)
write.csv(new_data2, paste(path_to_save_data,"categorized2.csv",sep=""), row.names=FALSE)


