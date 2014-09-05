angular.module('myApp.companies', [
	'btford.socket-io',
	'ui.router',
]).config(['$stateProvider', '$urlRouterProvider',
	function($stateProvider, $urlRouterProvider) {
		$stateProvider
			.state("company", {
				url: "/companies/{company_id:[0-9]{1,8}}",
				templateUrl: "/static/js/companies/Company.html",
				controller: "CompanyController"
			})
	}
]).controller('CompanyController', function($scope, $state, $rootScope, $log, $stateParams, ModelService) {
	$log.debug("i'm in CompanyController")
	ModelService.get_resource_item('Company', 'company', {company_id: parseInt($stateParams.company_id)});
	 $scope.$watch('company', function(newValue, oldValue) {
	 	if ((oldValue !== newValue)&&(newValue == null)){
      $state.transitionTo('404');
	 	}
   });
})