import sys

def main():

    ## check command line arguments
    num_args = len(sys.argv)
    if num_args != 3:
       print("usage: create_es_template <sensor_name> <field desc file>")
       sys.exit(1)

    ## retrieve command line arguments
    sensor_name = sys.argv[1]
    field_desc_file = sys.argv[2]

    ## read boilerplate for start of template
    start_es_template_file_name="start_es_template.txt"
    start_template_f=open(start_es_template_file_name, "r")
    if start_template_f.mode == 'r':
        start_template_txt = start_template_f.read()
    else:
        sys.stdout.write("could not read file %s" % start_es_template_file_name)
        sys.exit(1)

    ## read the description of fields file
    ## <field name>   : field with default type keyword
    ## <field name>,<field type> : field with type specified
    ## <field name>,<field type>,<qualifier name>=<qualifier value> : field name with type and qualifiers to the type
    f= open(field_desc_file,"r")
    if f.mode == 'r':
       sys.stdout.write(start_template_txt % (sensor_name, sensor_name, sensor_name))
       fl = f.readlines()
       ## line number and number of fields are not always the same because we skip blank lines
       num_fields = 0
       num_lines = 0
       for x in fl:
          num_lines = num_lines + 1
          stripped_line = x.strip()
          fields = stripped_line.split(",")
          if (len(stripped_line) > 0):
             if (num_fields > 0): 
                 print(", ") 
 
             ## col 0 = field name
             field_name = fields[0].strip()
             ## col 1 = field type or keyword by default
             field_type = "keyword"
             if (len(fields) > 1):
                 field_type = fields[1].strip()
                 
             sys.stdout.write("        \"%s\": {\n" % field_name)
             sys.stdout.write("          \"type\" : \"%s\"" % field_type)
   
             if (len(fields) <= 2):
                ## no additional qualifications for the field
                sys.stdout.write("\n")
             else:
                ## add comma separated qualifications: name=value
                qual_count = 0
                for qual_name_val in fields[2:]:
                   qual_pair = qual_name_val.split("=")
                   if (len(qual_pair) != 2):
                      sys.stderr.write("line %d: qualifier %s does not have name=value syntax" % (lines, qual_name_val)) 
                      sys.exit(1)
                   else:
                       print(", ") 
                       sys.stdout.write("          \"%s\" : \"%s\"\n" % (qual_pair[0].strip(), qual_pair[1].strip()))
              
             sys.stdout.write("        }")
             num_fields = num_fields + 1

       print
       print("      }")
       print("    }")
       print("  }")
       print("}")

if __name__== "__main__":
  main()
