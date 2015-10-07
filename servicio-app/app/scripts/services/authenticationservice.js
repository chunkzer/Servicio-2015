'use strict';

/**
 * @ngdoc service
 * @name servicioAppApp.authenticationservice
 * @description
 * # authenticationservice
 * Service in the servicioAppApp.
 */
angular
  .module('servicioAppApp')
  .service('AuthenticationService', AuthenticationService); 

    AuthenticationService.$inject = ['LocalStorageService', 'LocationService', '$rootScope', '$http', '$q'];

    function AuthenticationService(LocalStorageService, LocationService, $rootScope, $http, $q){
        this.credentials ={
            id: null,
            role: null,
            name: null
        };
        var self = this;
        
        this.validateSignedIn = function (){
            if(LocalStorageService && LocalStorageService.isAvailable()){
                var signedOut = LocalStorageService.get('signedOut');
                if(!!signedOut){
                    self.credentials = {};
                }else{
                    var tryId = LocalStorageService.get('id');
                    var tryRole = LocalStorageService.get('role');
                    var tryName = LocalStorageService.get('name');
                    if(!!tryId && !!tryRole && !!tryName){
                        self.credentials.id = tryId;
                        self.credentials.role = tryRole;
                        self.credentials.name = tryName;
                    }
                }
                
            }
        };
        this.validateSignedIn();

        return {      
            __wiki: {
            name: 'AuthenticationService',
            description: 'Permite hacer lo siguiente:<br>\n\
            <ul>\n\
            <li>Verificar si hay una sesión iniciada mediante <code>validate()</code>.</li>\n\
            <li>Obtener las credenciales actuales mediante <code>getCredentials()</code>.</li>\n\
            <li>Iniciar sesión mediante <code>signIn(username, password)</code>.</li>\n\
            <li>Cerrar sesión mediante <code>signOut()</code>.</li>\n\
            </ul><br>\n\
            Se apoya de <code>LocalStorageService</code> para almacenar y recuperar las credenciales.'
          },
            validate: function(){
                self.validateSignedIn();
                var session = !!self.credentials.id;
                
                if(!session){
                    $rootScope.$emit('signOut', {});
                    LocationService.set("/login");
                }
                return session;
            },
            getCredentials: function(){
                self.validateSignedIn();
                return self.credentials;
            },
            signIn: function(username, password){  
        
                var ADMIN = 0, CANDIDATE = 1;

                var defer = $q.defer();

                $http.post('/user_sessions', {
                  username: username,
                  password: password
                })
                .success(function(data, status){

                  LocalStorageService.clear();
                  self.credentials.id = data.id_user;

                  self.credentials.role = data.id_role;
                  self.credentials.name = data.full_name;

                  //I'm storing the credentials here only because it's easy for us only to open the url and be signed in
                  LocalStorageService.store('id', self.credentials.id);
                  LocalStorageService.store('role', self.credentials.role);
                  LocalStorageService.store('name', self.credentials.name);
                  defer.resolve();
                })
                .error(function(status){
                  defer.reject();
                });
                return defer.promise;

            },
            signOut: function(){
                LocalStorageService.clear();
                LocalStorageService.store("signedOut", "1");
                self.credentials = {
                    id: null,
                    role: null, 
                    name: null
                };
                return true;
            }
        
            
        };
    }

