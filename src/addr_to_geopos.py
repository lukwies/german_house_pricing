import pandas as pd
import numpy as np
import yaml
import time

from geopy.geocoders import Nominatim


if __name__ == '__main__':

	nom = Nominatim(user_agent='geopos')

	with open('../params.yaml') as file:
		config = yaml.safe_load(file)

	data = pd.read_csv(config['data']['csv_locations'])

	for i in range(len(data)):

		if 'lat' in data and not pd.isnull(data.loc[i, 'lat']):
			# There's already a geopos for this row
			continue

		try:
			loc  = data.loc[i,'location']
			plz  = data.loc[i,'plz']
			addr = '{} {}'.format(plz, loc)

			x = nom.geocode(addr)
			if x:
				data.loc[i,'lat'] = float(x.raw['lat'])
				data.loc[i,'lon'] = float(x.raw['lon'])
				print('\r{}/{}'.format(i,len(data)), end='')
			else:
				print("\rFailed to resolve: [" + addr + "]")
			time.sleep(1)

		except Exception as e:
			print("\nERROR: ", end="")
			print(e)
			break
		except KeyboardInterrupt:
			print("\nQuitting")
			break



	data.to_csv(config['data']['csv_geo_locations'], index=False)
	print("\nGeo data stored at " + config['data']['csv_locations'])
