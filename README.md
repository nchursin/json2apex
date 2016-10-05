#JSON2Apex 
####A Sublime Text 3 plugin to generate Salesforce Apex classes from JSON samples.

Ever developed a Salesforce integration with a huge JSON objects coming both ways? Even though you only need to do it ones it's pretty annoying to create a wrapper manually.
I've googled a tool for Apex class autogeneration from JSON sample, but found only 2 tools, none of which did satisfy me.
So I've made this.

###How to use it
Since I haven't published it to Package Control yet, in order to use you have to:

1. Clone this repo to `your_sublime_dir/Packages/`. Restart Sublime if needed
2. Get a JSON response or request sample
3. Open it in Sublime Text 3
4. Using `Ctrl+Shit+P` (or `⌘+Shift+P` on Mac) find `JSON2Apex: Convert sample to Apex`
5. Press Enter
6. Voila!

You've got formatted Apex class opened in a new buffer. You can change class names or just copy it to your project.

###Nearest future
Add a jumping between generated class names for easy renaming

###Other plans
1. Add XML convertion
2. Add generation from JSON schema
3. Online version