'use strict';

/**
 * @ngdoc overview
 * @name servicioAppApp
 * @description
 * # servicioAppApp
 *
 * Main module of the application.
 */
angular
  .module('servicioAppApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
//      .when('/', {
//        templateUrl: 'views/home.html',
//        controller: 'HomeCtrl'
//      })
      .when('/home', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl'
      })
      .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl'
      })
      .otherwise({
        redirectTo: '/home'
      });
  });
