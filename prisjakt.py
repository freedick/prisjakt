import requests
import json
import time
BASE_URL = "https://www.prisjakt.nu/"
SERVER_AJAX = "ajax/server.php"
SERVER_JSONAJAX = "ajax/jsonajaxserver.php"
FILTER_CLASS = "Category_Filter"
GRAPH_CLASS = "Graph_Product"
PRODUCT_SEARCH = "produkt_search"
PRICE_HISTORY_METHOD = "price_history"
GET_FILTER_METHOD = "get_filter"
def replace_bad_url(in_str):
	"""
		Converts ["&","=","?"] to hex to prevent bad urls
	"""
	BAD_SYMBOLS = ["&","=","?"]
	for symbol in symbols:
		in_str.replace(symbol, "%"+hex(ord(symbol))[2:])


"?class=Graph_Product&method=price_history&skip_login=1&product_id=2880218"
def ajax_request(http_params):
	"""
		Makes ajax request to prisjakt and returns response.
	"""
	response = requests.get(BASE_URL+SERVER_JSONAJAX, params=http_params)
	json_str = response.read()
	json_data = response.json()
	return json_data
def jsonajax_request(json_params):
	"""
		Makes a jsonajax request to prisjakt and returns response.
	"""
	default_json_params = {
		"visningslage":"lista",
		"order":"lokal_rank",
		"rev":"",
		"antal_produkter":"1759",
		"return_html":"true",
		"filter_layout_mode":"right",
	}
	for key in default_json_params:
		if not key in json_params:
			json_params[key]=default_json_params[key]
	http_params = {
		"m": PRODUCT_SEARCH,
		"p": json.dumps(json_params),
		"t": time.time(),
		"id":"2753", # Unknown...
	}
		
	response = requests.get(BASE_URL+SERVER_JSONAJAX, params=http_params)
	#JSON Data is preceded by "<!-- START JSON OUTPUT:\n"
	#(and succeeded by "\nEND JSON OUTPUT -->"
	json_data = json.loads(response.text[24:-20])
	return json_data
def get_category_data(category_id, columns):
	json_params = {
		"kategori_id":category_id,
		"kolumner":{ str(i) : str(column_id) for i,column_id in zip(range(len(columns)),columns)}
	}
	json_data = jsonajax_request(json_params)
	error = json_data['error']
	assert(error == False or error == "false")
	return json_data['result']

def get_product_history(product_id):
	ajax_params = {
		"class":GRAPH_CLASS,
		"method":PRICE_HISTORY_METHOD,
		"id":product_id,
	}
	results = ajax_request(ajax_params)
	return results
	
	
def get_category_filters(category_id):
	ajax_params = {
		"class":FILTER_CLASS,
		"method":GET_FILTER_METHOD,
		"id":category_id,
	}
	results = ajax_request(ajax_params)
	return results

def get_all_products(category_id, columns):
	category_data = get_category_data(category_id, columns)
	return category_data
def get_all_history(category_id, columns):
	columns = [2740,2741,775]
	category_id = "893"
	category_data = get_category_data(category_id, columns)
	product_ids = category_data[pids]
	

columns = [2740,775]
category = "893"
data = get_category_data(category, columns)
