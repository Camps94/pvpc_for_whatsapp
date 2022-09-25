"""
Example to use ESIOS
Copyright 2016 Santiago Peñate Vera <santiago.penate.vera@gmail.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from ESIOS_Library.ESIOS import *
from matplotlib import pyplot as plt
import urllib.request


def get_pvpc():

	start_ = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
	end_ = start_ + datetime.timedelta(days=1)
	token = '63aa79280f44132aa55c2b9b14f57bbe7faaf9f89230a2035715fa9342756bfc'
	esios = ESIOS(token)
	indicators_ = [1001]  # demand (MW) and SPOT price (€)
	df_list, names = esios.get_multiple_series(indicators_, start_, end_)
	df_merged = esios.merge_series(df_list, names)  # merge the DataFrames into a single one
	df = df_merged[names]  # get the actual series and neglect the rest of the info
	
return df.to_string()