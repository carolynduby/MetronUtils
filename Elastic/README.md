# Elastic Search Utils
# Create an Elastic Search template
## Usage 
```
python <sensor name> <field description file>
```
## Create an input file describing the fields of the sensor format 
The input is a CSV file.
Column 0: field name (omit boilerplate metron fields, i.e. ip_src_addr, ip_src_port, etc.  Boilerplate fields are added automatically.)
Column 1: type (optional: default is keyword)
Column 2 and up: additional name value pairs describing the type for example the format for a date field (optional: no qualifications by default)

For example, the test_fields input file below:

```
$ cat test_fields 
first_field
second_field,integer
third_field,date,format=epoch_millis
fourth_field,date,format=yyyy-MM-dd HH:mm:ss.SSS
```

## Run the command
```
python create_template.py test test_fields
```

Generates the following Elastic Search template PUT command:
```
PUT _template/test_index 
{
  "template": "test_index*",
  "settings": {
    
  },
  "mappings": {
    "test_doc": {
      "dynamic_templates": [
        {
          "geo_location_point": {
            "match": "enrichments:geo:*:location_point",
            "match_mapping_type": "*",
            "mapping": {
              "type": "geo_point"
            }
          }
        },
        {
          "geo_country": {
            "match": "enrichments:geo:*:country",
            "match_mapping_type": "*",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "geo_city": {
            "match": "enrichments:geo:*:city",
            "match_mapping_type": "*",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "geo_location_id": {
            "match": "enrichments:geo:*:locID",
            "match_mapping_type": "*",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "geo_dma_code": {
            "match": "enrichments:geo:*:dmaCode",
            "match_mapping_type": "*",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "geo_postal_code": {
            "match": "enrichments:geo:*:postalCode",
            "match_mapping_type": "*",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "geo_latitude": {
            "match": "enrichments:geo:*:latitude",
            "match_mapping_type": "*",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "geo_longitude": {
            "match": "enrichments:geo:*:longitude",
            "match_mapping_type": "*",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "timestamps": {
            "match": "*:ts",
            "match_mapping_type": "*",
            "mapping": {
              "type": "date",
              "format": "epoch_millis"
            }
          }
        },
        {
          "threat_triage_score": {
            "mapping": {
              "type": "float"
            },
            "match": "threat:triage:*score",
            "match_mapping_type": "*"
          }
        },
        {
          "threat_triage_reason": {
            "mapping": {
              "type": "text",
              "fielddata": "true"
            },
            "match": "threat:triage:rules:*:reason",
            "match_mapping_type": "*"
          }
        },
        {
          "threat_triage_name": {
            "mapping": {
              "type": "text",
              "fielddata": "true"
            },
            "match": "threat:triage:rules:*:name",
            "match_mapping_type": "*"
          }
        }
      ],
      "properties": {
        "source:type": {
          "type": "keyword"
        },
        "timestamp": {
          "type": "date",
          "format": "epoch_millis"
        },
        "guid": {
          "type": "keyword"
        },
        "alert": {
          "type": "nested"
        },
        "is_alert": {
          "type": "boolean"
        },
        "ip_src_addr": {
          "type": "keyword"
        },
        "ip_src_port": {
          "type": "keyword"
        },
        "ip_dst_addr": {
          "type": "keyword"
        },
        "ip_dst_port": {
          "type": "keyword"
        },
        "first_field": {
          "type" : "keyword"
        }, 
        "second_field": {
          "type" : "integer"
        }, 
        "third_field": {
          "type" : "date", 
          "format" : "epoch_millis"
        }, 
        "fourth_field": {
          "type" : "date", 
          "format" : "yyyy-MM-dd HH:mm:ss.SSS"
        }
      }
    }
  }
}
```
## Use the output
1. Open Kibana
2. Select Dev tools
3. Copy and paste the generated PUT command
4. Press the green arrow to install the template 
5. Check the output.
The output on the right panel of Dev Tools should look like this:
```
{
  "acknowledged": true
}
```


