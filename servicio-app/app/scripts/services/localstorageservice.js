'use strict';

/**
 * @ngdoc service
 * @name servicioAppApp.localstorageservice
 * @description
 * # localstorageservice
 * Service in the servicioAppApp.
 */
angular.module('servicioAppApp')
  .service('LocalStorageService', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
    return {
        isAvailable: function(){
            return typeof(Storage) !== "undefined"
        },
        store: function(key, value){
            if(this.isAvailable()){
                localStorage.setItem(key, value);
                return true;
            }
            return false;
        },
        modify: function (key, value){
            if(this.isAvailable()){
                if(this.remove(key)){
                    return this.store(key, value)
                }
                return false;
            }
            return false;
        },
        remove: function(key){
            if(this.isAvailable()){
                localStorage.removeItem(key);
                return true;
            }
            return false;
        },
        get: function(key){
            if(this.isAvailable()){
                return localStorage.getItem(key);
            }
            return null;
        },
        clear: function(){
            if(this.isAvailable){
                localStorage.clear();
                return true;
            }
            return false;
        }
    };
  });
