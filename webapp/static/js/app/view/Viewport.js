Ext.define('NOAH.view.Viewport', {
    extend: 'Ext.container.Viewport',
    layout: 'fit',

    requires: [
        'Ext.layout.container.Border',
        'Ext.resizer.Splitter',
        'NOAH.view.Navbar',
        'NOAH.view.Map',
    ],

    initComponent: function() {
        var me = this;

        Ext.apply(me, {
            id: 'app-viewport',
            layout: {
                type: 'border',
                padding: '0 50 50 50' // pad the layout from the window edges
            },
            /*
            items: [{
                xtype: 'panel',
                border: false,
                layout: 'border',
                dockedItems: [
                    Ext.create('NOAH.view.Navbar')
                ],
            }]*/
            items: [{
                id: 'app-header',
                xtype: 'box',
                region: 'north',
                height: 100,
                html: 'Ext Portal'
            },
            {
                xtype: 'panel',
                border: false,
                region: 'center',
                layout: 'fit',
                dockedItems: [
                    Ext.create('NOAH.view.Map')
                ],
            }]
        });

        me.callParent(arguments);
    }
});