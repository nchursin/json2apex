# JSON2Apex 
#### A Sublime Text 3 plugin to generate Salesforce Apex classes from JSON samples.

## Description
A tool to generate Apex code from JSON. You can use it to generate an Apex class either from a API resposne/request sample or from predefined schema.

## Requirements
1. Sublime Text 3
2. [MavensMate](http://mavensmate.com/ "MavensMate") is highly recommended. This plugin uses MM's Apex syntax highlight.

Since MavensMate requires ST 3, there will be no ST 2 support.

## Installation
### Via Package Control
Install [Package Control](https://packagecontrol.io/installation) if you don't have it.

1. Run `Install Package`
2. Search for `JSON2Apex`
3. Press `Enter`

### Manual

1. Clone this repo to your Sublime Packages folder. To find it go to `Preferences -> Browse Packages` (`Sublime Text -> Preferences -> Browse Packages` on Mac).
2. Restart Sublime if needed.

## How to use it
### Generate class from JSON API request/response sample
1. Get a JSON response or request sample
2. Open it in Sublime Text 3
3. Using `Ctrl+Shit+P` (or `⌘+Shift+P` on Mac) find `JSON2Apex: Convert sample to Apex`
4. Press Enter
5. You will see generated Apex code. Also a text input appears at the bottom of the buffer. Use this input to change generated class names quickly.

### Generate class from JSON or YAML schema
JSON sample schema can be found [here](https://github.com/nchursin/json2apex/blob/master/schema_sample.json "JSON Schema")
YAML sample schema can be found [here](https://github.com/nchursin/json2apex/blob/master/schema_sample.yaml "YAML Schema")

1. Create a schema.
2. Use `JSON2Apex: Convert JSON schema to Apex` (`JSON2Apex: Convert YAML schema to Apex` for YAML schemas) command. (`Ctrl+Shit+P` (or `⌘+Shift+P` on Mac) to find it)
3. Rename the class either manually or using a text input at the bottom of the buffer.

After renaming is over Sublime will select all the generated code for you to copy it anywhere you want.

## Future plans

1. Swagger JSON to Apex REST Definition generation.

## License

MIT except for pyyaml.