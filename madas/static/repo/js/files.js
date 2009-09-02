Ext.madasFilesInit = function() {
    var expId = Ext.madasCurrentExperimentId();

    //reload trees
    Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
    
    Ext.getCmp('pendingFilesTree').getLoader().load(Ext.getCmp('pendingFilesTree').getRootNode());
}

Ext.madasFiles = {
baseCls: 'x-plain',
border:'false',
layout:'fit',
defaults: {
    //bodyStyle:'padding:15px;background:transparent;'
},
items:[
       {
       title: 'files',
       //       bodyStyle:'padding:0px;background:transparent;',
       collapsible: false,
       layout:'border',
       items: [
               {
               xtype:'treepanel',
               border: false,
               autoScroll: true,
               id:'filesTree',
               enableDD: true,
               animate: true,
               region:'center',
               useArrows: true,
               dropConfig: { appendOnly: true },
               dataUrl:wsBaseUrl + 'files',
               requestMethod:'GET',
               root: {
                   nodeType: 'async',
                   text: 'experiment',
                   draggable: false,
                   id: 'experimentRoot'
               },
               //tbar: [{
//                      text: 'add files',
//                      cls: 'x-btn-text-icon',
//                      icon:'static/repo/images/add.gif',
//                      handler : function(){
////                      userStore.add(new Ext.data.Record({'user':'', 'type':'1', 'additional_info':''}));
//                      }
//                      }
//                      ],
               listeners:{
                    render: function() {
                        Ext.getCmp('filesTree').getLoader().on("beforeload", function(treeLoader, node) {
                            treeLoader.baseParams.experiment = Ext.madasCurrentExperimentId();
                            }, this);
                        Ext.getCmp('filesTree').getRootNode().expand();
                    },
               nodedrop: function(de) {
                    Ext.Ajax.request({
                                     method:'GET',
                                url: wsBaseUrl + 'moveFile',
                                     success: function() { alert('moved'); },
                                     failure: function() { alert('failed'); },
                                headers: {
//                                'my-header': 'foo'
                                },
                                     params: { file: de.dropNode.id, target: de.target.id, experiment_id: Ext.madasCurrentExperimentId() }
                                });
               }
                }
               },
               
               {
               xtype:'treepanel',
               //bodyStyle:'padding:0px;background:transparent;',
               autoScroll: true,
               split:true,
               id:'pendingFilesTree',
               enableDD: true,
               region:'east',
               width:200,
               title:'pending files',
               collapsible:true,
               titleCollapse:false,
               animate: true,
               useArrows: true,
               dropConfig: { allowContainerDrop: false },
               dataUrl:wsBaseUrl + 'pendingfiles',
               requestMethod:'GET',
               root: {
               nodeType: 'async',
               text: 'pending files',
               draggable: false,
               id: 'pendingRoot'
               },
               listeners:{
               render: function() {
               Ext.getCmp('pendingFilesTree').getRootNode().expand();
               },
               nodedrop: function(de) {
               console.log(de);
               }
               }
               }
               ]
       }
       ]
};