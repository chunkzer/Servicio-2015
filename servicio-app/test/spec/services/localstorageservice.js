'use strict';

describe('Service: localstorageservice', function () {

  // load the service's module
  beforeEach(module('servicioAppApp'));

  // instantiate service
  var localstorageservice;
  beforeEach(inject(function (_localstorageservice_) {
    localstorageservice = _localstorageservice_;
  }));

  it('should do something', function () {
    expect(!!localstorageservice).toBe(true);
  });

});
