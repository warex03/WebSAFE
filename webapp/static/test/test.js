angular.module('test', ['ui.bootstrap'])
    .config(testRouteConfig);
    
function testRouteConfig($routeProvider){
    $routeProvider
    .when('/', {
        controller: ListCtrl,
        templateUrl: 'list'
    })
    .when('/view/:id', {
        controller: DetailCtrl,
        templateUrl: 'detail'
    })
    .otherwise({redirectTo: '/'})
}