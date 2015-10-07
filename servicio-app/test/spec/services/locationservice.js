'use strict';

describe('Service: locationservice', function () {

  // load the service's module
  beforeEach(module('servicioAppApp'));

  // instantiate service
  var locationservice;
  beforeEach(inject(function (_locationservice_) {
    locationservice = _locationservice_;
  }));

  it('should do something', function () {
    expect(!!locationservice).toBe(true);
  });

});
