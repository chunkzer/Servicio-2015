'use strict';

/**
 * @ngdoc function
 * @name servicioAppApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the servicioAppApp
 */
angular.module('servicioAppApp')
  .controller('LoginCtrl', function ($scope, AuthenticationService, LocationService) {
    if($scope.__wiki){
      this.__wiki = {
        name: "LoginCtrl",
        description: "Contiene la funcion <code> doLogin() </code>, que sanitiza los valores de \n\
        username y password, verifica que los campos no esten vacios e inicia sesion con <code> \n\
        AuthenticationService.signIn() </code>. <br> Si las credenciales son correctas se redirige \n\
        hacia /home."
      }
      return;
    }
    
    var ADMIN = 0, CANDIDATE = 1;
    
    if(AuthenticationService.validate()){
      if(AuthenticationService.getCredentials().role == CANDIDATE){
          LocationService.set("/candidato");
          
      } else{
      LocationService.set("/home");
      }
    }
    
    $scope.username = '';
    $scope.password = '';
    
    $scope.doLogin = function (){
        
      $scope.username = $scope.username.replace(/'/g, "").replace(/\"/g, "");
      $scope.password = $scope.password.replace(/'/g, "").replace(/\"/g, "");

      if($scope.username == '' || $scope.password == ''){
        alert("El campo de nombre de usuario o de contrasena esta vacio.");
        return false;
      }
    AuthenticationService.signIn($scope.username, $scope.password).then(function(success){
        $scope.$emit('signedIn', {});
        LocationService.set('/home');
    }, function(error){
        alert("Nombre de usuario o contrasena incorrecto.");
      });
    };
  });
