angular.module('myApp', [
  'btford.socket-io',
  'ui.router',
  'myApp.companies'
]).factory('socket', function(socketFactory) {
  return socketFactory({
    ioSocket: io.connect('/test')
  });
}).service('ModelService', function($rootScope, $log, socket) {
  $rootScope.msgs = []
  var request = function(request_type, resource, local_resource, params_dict) {
    socket.emit(request_type, {
      resource: resource,
      local_resource: local_resource,
      params: params_dict
    });
    return 0;
  };
  this.get_resource = function(resource, local_resource, params_dict) {
    return request('recource_get', resource, local_resource, params_dict)
  };
  this.get_resource_item = function(resource, local_resource, params_dict) {
    return request('recource_item_get', resource, local_resource, params_dict)
  };

  socket.on('recource_get', function(msg) {
    $log.debug(msg);
    $rootScope[msg.local_resource] = angular.fromJson(msg.data);
  });
  socket.on('my response', function(msg) {
    $rootScope.msgs.push(msg);
  });
}).controller('TTT',
  function($scope, $rootScope, $log, ModelService) {
    ModelService.get_resource('Company', 'companies', {});
    $log.debug("I'm in TTT");

  }).config(['$stateProvider', '$urlRouterProvider',
  function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
      .state("home", {
        url: "/",
        template: '<p class="lead ng-scope">Welcome to the UI-Router Demo</p>',
        controller: "TTT"
      })
      .state("404", {
        url: "/404",
        template: '<p class="lead ng-scope">Page no exists !!!!</p>',
        controller: "TTT"
      });
  }
]);