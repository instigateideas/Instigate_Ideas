## Data From Teltonika Device
data = "00000000000004d60813000001779a2b6c28002f640b5106ed715d003f01510f0000000c05ef00f0001503c800450105b50005b60003420000430dd044000002f100009dfb100000000000000001779a2b6c32002f640b5106ed715d003f01510f0000f00c05ef00f0011503c800450105b50005b60003420000430dcf44000002f100009dfb100000000000000001779a2cdf40002f640b5106ed715d003f01510f0000f00c05ef00f0001503c800450105b50005b60003420000430dce44000002f100009dfb100000000000000001779a2d2d60002f640b5106ed715d003f01510f0000f00c05ef00f0011503c800450105b50005b60003420000430dd044000002f100009dfb100000000000000001779a2e1f90002f640b5106ed715d003f01510e0000f00c05ef00f0001503c800450105b50005b60003420000430dca44000002f100009dfb100000000000000001779a38a6e0002f640b5106ed715d003f01510f0000f00c05ef00f0011503c800450105b50005b60003420000430db344000002f100009dfb100000000000000001779a38e178002f640b5106ed715d003f01510f0000ef0c05ef01f0011503c800450105b50005b6000342368a430e0244008702f100009dfb100000000000000001779a3a1228002f6407ef06ed73b600300137110000f00c05ef01f0001504c800450105b50004b600024236ff430e4d44008c02f100009dfb100000000000000001779a3d4e48002f6407ef06ed73b600300137100000f00c05ef01f0011503c800450105b50004b6000342387c430e7044008c02f100009dfb100000000000000001779a3e4460002f6407ef06ed73b600300137100000f00c05ef01f0001503c800450105b50004b6000342383d430e7644008c02f100009dfb100000000000000001779a44b8b8002f6407ef06ed73b600300137110000f00c05ef01f0011503c800450105b50004b6000342377a430e9e44008c02f100009dfb100000000000000001779a45a700002f6407ef06ed73b600300137100000f00c05ef01f0001503c800450105b50004b600034237ca430ea644008c02f100009dfb100000000000000001779a464ef8002f640b7306ed7513002f001d110000f00c05ef01f0011503c800450105b50004b60003423c17430eab44008c02f100009dfb100000000000000001779a473d40002f640b7306ed7513002f001d0f0000f00c05ef01f0001503c800450105b50004b60003423817430eb444008c02f100009dfb100000000000000001779a49ecc0002f640b7306ed7513002f001d100000f00c05ef01f0011503c800450105b50004b60003423849430ed044008c02f100009dfb100000000000000001779a4adef0002f640b7306ed7513002f001d100000f00c05ef01f0001503c800450105b50004b600034237cf430ed944008c02f100009dfb100000000000000001779a56a2a8002f6408c806ed742a003a012e110000000c05ef01f0001503c800450105b50004b600034236ef430f7144008c02f100009dfb100000000000000001779a56a2b2002f6408c806ed742a003a012e110000f00c05ef01f0011503c800450105b50004b600034236f2430f7144008c02f100009dfb100000000000000001779a5790f0002f6408c806ed742a003a012e0f0000f00c05ef01f0001503c800450105b50005b600034236cb430f7f44008c02f100009dfb1000000000001300003b2c"

data_1 = "000000000000008c08010000013feb55ff74000f0ea850209a690000940000120000001e09010002000300040016014703f0001504c8000c0900730a00460b00501300464306d7440000b5000bb60007422e9f180000cd0386ce000107c700000000f10000601a46000001344800000bb84900000bb84a00000bb84c000000024e0000000000000000cf00000000000000000100003fca"

import pandas as pd
import time
import json

class Parser(object):
	def __init__(self):
		self.four_zeros_length = 4
		self.data_feild_length = 4
		self.codec_id_length = 1
		self.number_of_data_1_len = 1
		self.number_of_data_2_len = 1
		self.mapping_data = self.get_mapper_data()
		self.crc_16_len = 4
		self.parsed_data = {}


	def read_master_table(self):
		data_df = pd.read_excel('./master_table.xlsx')
		dat = data_df.apply(lambda x: [x.dropna()], axis=1).to_json()

		return json.loads(dat)

	def get_mapper_data(self):
		master_data = self.read_master_table()
		new_dict = {}
		for k, v in master_data.items():
			new_dict[master_data[k][0]["AVL ID"]] = master_data[k]

		return new_dict

	def check_key(self, mapped_data, key):
		try:
			desc = mapped_data[0][key]
		except:
			desc = None	

		return desc


	def convert_epoch(self, epoch_val):
		return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(epoch_val)/1000))

	def flaten_dict(self, dict_val):
		pass

	def avl_data_json(self, json_data):
		data = json_data["avl_data"]
		print("Total AVL Data to Flatened: ", len(data))
		final_data = []
		a = 0
		for datum in data:
			new_dict = {}
			
			no_of_rec = datum["element_record_conv"]
			print("Number of Records: ", no_of_rec)
			for k, v in datum.items():
				if k != "io_element_records":
					new_dict[k] = datum[k]
				else:
					iter_val = 1
					for ind, rec in enumerate(datum[k]):
						for record in rec["avl_records"]:
							kv = "rec_{}_of_{}".format(iter_val, no_of_rec+1)
							temp_dict = new_dict.copy()
							temp_dict["rec_iter"] = kv
							temp_dict.update(record)
							iter_val = iter_val + 1
							final_data.append(temp_dict)
							temp_dict = {}			

		return final_data

	def name_desc_value_mapper(self, rec_id, rec_val):
		mapped_data = self.mapping_data[rec_id]
		name = self.check_key(mapped_data, "Name")
		name_desc = self.check_key(mapped_data, "Description")
		value_desc = self.check_key(mapped_data, str(rec_val))

		return name, name_desc, value_desc

	def data_slicer(self, datum, field_length, initial_pos=0, byte=2):
		if initial_pos == 0:
			cut_length = field_length*byte
			datum = datum[initial_pos: cut_length]
			next_pos = cut_length
		else:
			cut_length = field_length*byte
			end_pos = cut_length + initial_pos
			datum = datum[initial_pos: end_pos]
			next_pos = end_pos

		return datum, next_pos

	def hex_to_decimal(self, val):
		decimal_val = int(val, 16) 

		return decimal_val

	def convert_to_df(self, data_df):
		temp_df = pd.DataFrame(data_df)

		return temp_df

	def crc_16_parser(self, data, pos):
		crc_16, pos = self.data_slicer(datum=data, field_length=self.crc_16_len, initial_pos=pos)
		print("CRC-16 Data: ", crc_16)

		return crc_16, pos


	def io_element_parser(self, data, num_io_records, pos, avl_datum):
		num_records = self.hex_to_decimal(num_io_records)
		print("AVL Records Count: {} ==> {}".format(num_io_records, num_records))
		avl_datum["element_record_conv"] = num_records
		record_bytes = [1, 2, 4, 8, 16, 32, 64]
		iter_val = 0
		breaker = 0
		avl_datum["io_element_records"] = []
		
		for i in range(num_records):
			data_io = {}
			io_element, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
			data_io["num_io_element"] = io_element
			number_of_elements = self.hex_to_decimal(io_element)
			data_io["num_io_element_conv"] = number_of_elements
			record_byte = record_bytes[iter_val]
			print("\n~~~~~~~~~~~~~~~~~~~~~~~ I/O Element-{} ==> {} Bytes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(i+1, record_byte))
			print("{}b Element Count {} ==> {}: ".format(record_byte, io_element, number_of_elements))
			data_io["element_byte"] = record_byte
			data_records = []
			for element in range(number_of_elements):
				element_id, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
				element_id_conv = self.hex_to_decimal(element_id)
				print("Element Record ID: {} ==> {}".format(element_id, element_id_conv))
				element_value, pos = self.data_slicer(datum=data, field_length=record_byte, initial_pos=pos)
				element_value_conv = self.hex_to_decimal(element_value)
				print("Element Record Value {} ==> {}".format(element_value, element_value_conv))
				name, name_desc, value_desc = self.name_desc_value_mapper(rec_id=element_id_conv, rec_val=element_value_conv)
				data_records.append({"record_id": element_id, "record_id_conv": element_id_conv, "record_byte": record_byte,"record_value": element_value, "record_value_conv": element_value_conv, "name": name, "name_desc": name_desc, "value_desc": value_desc})
				breaker+= 1
				print("Breaker ==> {}".format(breaker))
			data_io["avl_records"] = data_records
			avl_datum["io_element_records"].append(data_io)
			if num_records == breaker:
				print("\n~~~~~~~~~~~~~~~~~~~~~~~ I/O Element-{} ==> 8 Bytes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(i+2, record_byte))
				data_io = {}
				data_io["num_io_element"] = None
				data_io["num_io_element_conv"] = None
				data_io["element_byte"] = 8
				data_records = [] # Intialize to before break

				b8_element_count, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
				print("8b Element Count: {} ==> {}".format(b8_element_count, self.hex_to_decimal(b8_element_count)))
				data_records.append({"record_id": None, "record_id_conv": None, "record_byte": 8,"record_value": b8_element_count, "record_value_conv": self.hex_to_decimal(b8_element_count)})
				data_io["avl_records"] = data_records
				avl_datum["io_element_records"].append(data_io)
				break
			iter_val = iter_val + 1

		return avl_datum, pos 


	def avl_data_parser(self, data, pos):
		print("\n ******************* AVL Data ****************************")
		avl_datum = {}
		timestamp, pos = self.data_slicer(datum=data, field_length=8, initial_pos=pos)
		print("Timestamp: ", timestamp)
		avl_datum["timestamp"] = timestamp
		avl_datum["timestamp_conv"] = self.convert_epoch(self.hex_to_decimal(timestamp))
		priority, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
		print("Priority: ", priority)
		avl_datum["priority"] = priority
		avl_datum["priority_conv"] = self.hex_to_decimal(priority)
		longitude, pos = self.data_slicer(datum=data, field_length=4, initial_pos=pos)
		print("Longitude: ", longitude)
		avl_datum["longitude"] = longitude
		avl_datum["longitude_conv"] = self.hex_to_decimal(longitude)
		latitude, pos = self.data_slicer(datum=data, field_length=4, initial_pos=pos)
		print("Latitude: ", latitude)
		avl_datum["latitude"] = latitude
		avl_datum["latitude_conv"] = self.hex_to_decimal(latitude)
		altitude, pos = self.data_slicer(datum=data, field_length=2, initial_pos=pos)
		print("Altitude: ", altitude)
		avl_datum["altitude"] = altitude
		avl_datum["altitude_conv"] = self.hex_to_decimal(altitude) 
		angle, pos = self.data_slicer(datum=data, field_length=2, initial_pos=pos)
		print("Angle: ", angle)
		avl_datum["angle"] = angle
		avl_datum["angle_conv"] = self.hex_to_decimal(angle)
		satelite, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
		print("Satelite: ", satelite)
		avl_datum["satelite"] = satelite
		avl_datum["satelite_conv"] = self.hex_to_decimal(satelite)
		speed, pos = self.data_slicer(datum=data, field_length=2, initial_pos=pos)
		avl_datum["speed"] = speed
		avl_datum["speed_conv"] = self.hex_to_decimal(speed)
		print("Speed: ", speed)
		print("###### I/O Elements ######")
		io_id, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
		print("Event ID: ", io_id)
		avl_datum["event_id"] = io_id
		element_record, pos = self.data_slicer(datum=data, field_length=1, initial_pos=pos)
		avl_datum["element_record"] = element_record
		print("Event Count: ", element_record)
		avl_datum, pos = self.io_element_parser(data=data, num_io_records=element_record, pos=pos, avl_datum=avl_datum)

		return avl_datum, pos, 


	def teltonika_parser(self, data):
		four_zeros, pos = self.data_slicer(datum=data, field_length=self.four_zeros_length)
		self.parsed_data["four_zeros"] = four_zeros
		print("Four Zeros data: ", four_zeros)
		data_field, pos = self.data_slicer(datum=data, field_length=self.data_feild_length, initial_pos=pos)
		self.parsed_data["data_field"] = data_field
		print("Data Field: ", data_field)
		codec_id, pos = self.data_slicer(datum=data, field_length=self.codec_id_length, initial_pos=pos)
		self.parsed_data["codec_id"] = codec_id
		print("Codec ID: ", codec_id)
		number_of_data_1, pos = self.data_slicer(datum=data, field_length=self.number_of_data_1_len, initial_pos=pos)
		self.parsed_data["number_of_data_1"] = number_of_data_1
		avl_data_count_1 = self.hex_to_decimal(number_of_data_1)
		self.parsed_data["number_of_data_1_conv"] = avl_data_count_1
		print("AVL Data Count 1: {} ==> {}".format(number_of_data_1, avl_data_count_1))
		self.parsed_data["avl_data"] = []
		for iter_ in range(avl_data_count_1):
			str_position = pos
			avl_datum, pos = self.avl_data_parser(data=data, pos=str_position)
			self.parsed_data["avl_data"].append(avl_datum)
		avl_data_count_2, pos = self.data_slicer(datum=data, field_length=self.number_of_data_2_len, initial_pos=pos)
		print("AVL Data Count 2: {} ==> {}".format(avl_data_count_2, self.hex_to_decimal(avl_data_count_2)))
		self.parsed_data["number_of_data_2"] = avl_data_count_2
		self.parsed_data["number_of_data_2_conv"] = self.hex_to_decimal(avl_data_count_2)
		crc, pos = self.crc_16_parser(data=data, pos=pos)
		self.parsed_data["crc_16"] = crc
		print("Validate Parsing: ", len(data[pos:]))
		print("Existing out of loop parsed the data")

		return self.parsed_data

parser = Parser()
final_data = parser.teltonika_parser(data=data)
flaten_json = parser.avl_data_json(json_data=final_data)
data_df = parser.convert_to_df(flaten_json)
print(data_df.columns)
data_df.to_csv("data_table.csv")
#print(final_data)
