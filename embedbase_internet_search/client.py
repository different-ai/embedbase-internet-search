from embedbase_client.client import EmbedbaseClient
 
embedbase = EmbedbaseClient('http://localhost:8000')

dataset_id = 'product-ads'
question = 'im looking for a nice pant that is comfortable and i can both use for work and for climbing'
s = embedbase.dataset(dataset_id).search(question)
print(s)
