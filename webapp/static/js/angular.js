var calculateApp = angular.module('calculate', ['ui.bootstrap', 'mapApp', 'calculate.directives']);
calculateApp.factory('Exposure', function(){
    return {};
});
calculateApp.factory('Hazard', function(){
    return {};
});
angular.module('mapApp', []);

function RouteConfig($routeProvider){
/*
    $routeProvider
    .when('/', {
        controller: ListCtrl,
        templateUrl: 'list'
    })
    .otherwise({redirectTo: '/'})
    
    $locationProvider.html5Mode(true);
    */
}