library(httr)
dataset="/Users/user/Desktop/text-mining/VariableCibles.csv"
path_to_save_data='/Users/user/Desktop/'

url <- "http://127.0.0.1:8000/api/correction"
result_correction = content(POST(url,body = list(file = dataset,target="profession")))

#result to dataframe
new_data <- as.data.frame(do.call(cbind, result_correction$file))

#change list class to character in the dataframe
new_data$profession <- unlist(new_data$profession, use.names = FALSE)
new_data$Corrected <- unlist(new_data$Corrected, use.names = FALSE)

#save dataframe as csv
write.csv(new_data, paste0(path_to_save_data,"corrected.csv"), row.names=FALSE)


url2 <- "http://127.0.0.1:8000/api/categorization"
list_professions <- paste("menagere","enseignement","administration","commerce","medical","eleveurs")
result_categorization = content(POST(url2, body = list(file = "/Users/user/Desktop/corrected.csv",target="profession",elements=list_professions)))


new_data2 <- as.data.frame(do.call(cbind, result_categorization$categorized_dataset))
new_data2$profession <- unlist(new_data2$profession, use.names = FALSE)
new_data2$Corrected <- unlist(new_data2$Corrected, use.names = FALSE)
new_data2$Categorie <- unlist(new_data2$Categorie, use.names = FALSE)
write.csv(new_data2, paste0(path_to_save_data,"categorized2.csv"), row.names=FALSE)



