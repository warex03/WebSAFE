Ext.define('NOAH.view.Navbar', {
    extend: 'Ext.Component',

    dock: 'top',
    baseCls: 'cf-header',

    initComponent: function() {
        Ext.applyIf(this, {
            html: 'DOST Project NOAH'
        });

        this.callParent(arguments);
    }
});