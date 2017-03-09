#Not working. Fix in development

#JSON2Apex 
####A Sublime Text 3 plugin to generate Salesforce Apex classes from JSON samples.

##Description
A tool to generate Apex code from JSON. You can use it to generate an Apex class either from a API resposne/request sample or from predefined schema.

##Installation
###Manual
Clone this repo to `your_sublime_dir/Packages/`. Restart Sublime if needed.

##How to use it
###Generate class from JSON API request/response sample
1. Get a JSON response or request sample
2. Open it in Sublime Text 3
3. Using `Ctrl+Shit+P` (or `⌘+Shift+P` on Mac) find `JSON2Apex: Convert sample to Apex`
4. Press Enter
5. You will see generated Apex code. Also a text input appears in the bottom of the buffer. Use this input to change generated class names quickly.

###Generate class from JSON schema
Sample schema can be found [here](https://github.com/nchursin/json2apex/blob/master/schema_sample.json "Schema Sample")

1. Create a schema. 
2. Use `JSON2Apex: Convert JSON schema to Apex` command. (`Ctrl+Shit+P` (or `⌘+Shift+P` on Mac) to find it)
3. Rename the class either manually or using a text input in the bottom of the buffer.

Currently the plugin will generate methods only for interfaces from the `System` namespace. 

After renaming is over Sublime will select all the generated code for you to copy it anywhere you want.

##Future plans

1. Swagger JSON to Apex REST Definition generation
2. YAML schemas support