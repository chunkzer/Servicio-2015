# Servicio-2015

This is the source code of UNISON's Math deparment contest administrator. 

## Front end setup

This is an AngularJS application.

### Requirements

+ npm
+ bower
+ IDE / Editor

### Setup

1. Go to the folder /servicio-app
2. Run `npm install`. node_modules folder should be created.
3. Run `bower install`. bower_components folder should be created.

### Yeoman

Front end uses [yo angular generator] (https://github.com/yeoman/generator-angular) template for AngularJS, so you can use *yo angular* to add controllers, services, directives, etc  to the source code.

Here's a short Yeoman tutorial: http://yeoman.io/codelab/setup.html

### Build & development

Run `grunt serve` to test changes in localhost:9000

### Testing

Running `grunt test` will run the unit tests with karma.

