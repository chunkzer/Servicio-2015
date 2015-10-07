'use strict';

/**
 * @ngdoc function
 * @name servicioAppApp.controller:HomeCtrl
 * @description
 * # HomeCtrl
 * Controller of the servicioAppApp
 */
angular.module('servicioAppApp')
  .controller('HomeCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
