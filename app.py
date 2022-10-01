import os
import requests

from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
base_url = "https://www.guesehat.com/"

class Index(Resource):
	def get(self):
		api_title = "List Of Disease"
		api_desc = "This API provided list of disease with the description, symptomps, prevention, root cause, diagnosis, treatment"
		api_routes = {"list-of-disease": "http://127.0.0.1:5000/disease",
						"detail-disease": "http://127.0.0.1:5000/disease/<str:disease_name>"}

		return {"api_title": api_title,"api_desc": api_desc, 
				"api_data_source": base_url, "api_routes": api_routes}


class Disease(Resource):
	def get(self: object) -> dict:
		url = os.path.join(base_url, "nama-penyakit-a-z")
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		context = list()

		for disease in soup.find_all(class_="dislist-body-link"):
			disease_url = disease["href"]
			disease_url = disease_url.replace(base_url, "http://127.0.0.1:5000/disease/")

			if not disease_url:
				disease_url = "-"

			context.append({"disease_name": disease.text, "api_link_detail": disease_url})
		return context


class DiseaseDetail(Resource):
	def get(self: object, disease_name: str) -> dict:
		url = os.path.join(base_url, disease_name)
		context = dict()

		page = requests.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		details = soup.find_all(class_="obat-group-head")

		for detail in details:
			try:
				detail_text = "".join([i.get_text() for i in detail_text.find_all("span")])
			except:
				detail_text = detail.find("p")
				detail_text = "".join([i.get_text() for i in detail_text.find_all("p")])

			li_categories = detail.find_all("li")
			try:
				detail_text += "".join(li.find("span").text for li in li_categories)
			except:
				try:
				    detail_text += "".join(li.find("p").text for li in li_categories)
				except:
				    detail_text += "".join(li.text for li in li_categories)

			context[detail.find("h2").text.lower()] = detail_text
		return context


# routes
api.add_resource(Index, "/")
api.add_resource(Disease, "/disease")
api.add_resource(DiseaseDetail, "/disease/<string:disease_name>")

if __name__ == "__main__":
	app.run(debug=True)