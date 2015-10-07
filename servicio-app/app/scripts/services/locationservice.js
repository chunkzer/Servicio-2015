'use strict';

/**
 * @ngdoc service
 * @name servicioAppApp.locationservice
 * @description
 * # locationservice
 * Service in the servicioAppApp.
 */
angular.module('servicioAppApp')
  .service('LocationService', function ($window) {
    var self = this;
    var initialDomain = $window.location.href.replace("http://", "").replace("https://", "").split("/")[0];
    
    self.domain = initialDomain + "/#";
    self.protocol = "http";
    
        return {
      __wiki: {
        name: "LocationService",
        description: "Se encarga de obtener la url actual (con o sin dominio incluido) así como de actualizar la misma. Sus métodos principales\n\
        son <code>set(path)</code> que permite cambiar la url especificando el path (sin dominio) y <code>get(includeDomain)</code> que devolverá\n\
        la url actual (con dominio si se pasa <code>true</code> como parámetro)"
      },
      __buildUrl: function (){
          return self.protocol + "://" + self.domain;
      },
      setProtocol: function(protocol){
        self.protocol = protocol;
        return true;
      },
      setDomain: function(domain){
        self.domain = domain;
        return true;
      },
      set: function(path){
        $window.location.href = this.__buildUrl()  + path;
        return true;
      },
      get: function(includeDomain){
        if(includeDomain){
          return $window.location.href;
        }
        return $window.location.href.replace(this.__buildUrl(), "");
      }
    };
    // AngularJS will instantiate a singleton by calling "new" on this function
  });
