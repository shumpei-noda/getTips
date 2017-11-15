PY = python3
LT = 35.705358
LG = 139.731072
WIDTH = 1
COL_SIZE = 10
ROW_SIZE = 10
SEARCH_PARAMS_PATH = search_parameter\/params_$(LT)_$(LG)_$(WIDTH)_$(COL_SIZE)_$(ROW_SIZE).json
IDS_PATH = $(subst search_parameter,ids,$(subst params,ids,$(SEARCH_PARAMS_PATH)))

.PHONY: get_ids split get_search_parameter_path get_ids_path test

test:
	$(MAKE) split
	$(MAKE) get_ids
	$(PY) get_id_num_ave_sum_max.py $(IDS_PATH)


get_ids: get_ids.py
	$(PY) get_ids.py $(SEARCH_PARAMS_PATH)\
		> $(IDS_PATH)

.SILENT:
split: get_search_area.py index.html
	$(PY) get_search_area.py --center_latitude=$(LT)\
			--center_longitude=$(LG) \
			--width=$(WIDTH) \
			--column_size=$(COL_SIZE) \
			--row_size=$(ROW_SIZE) \
			> $(SEARCH_PARAMS_PATH)
	grep -l 'HOGE.json' index.html | xargs sed -i.bak -e 's/HOGE.json/$(SEARCH_PARAMS_PATH)/g'
	open -a safari index.html
	cat index.html.bak > index.html
	rm	index.html.bak


get_search_parameter_path:
	@echo $(SEARCH_PARAMS_PATH)

get_ids_path:
	@echo $(IDS_PATH)
