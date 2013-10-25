angular.module('test', ['ui.bootstrap'])
    .config(testRouteConfig);
    
function testRouteConfig($routeProvider, $locationProvider){
    $routeProvider
    .when('/test', {
        controller: ListCtrl,
        templateUrl: 'list'
    })
    .when('/view/:id', {
        controller: DetailCtrl,
        templateUrl: 'detail'
    })
    .otherwise({redirectTo: '/test'})
    
    //$locationProvider.html5Mode(true);
}