MA.FilesInit = function() {
    var expId = MA.CurrentExperimentId();

    //reload trees
    Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
    
    Ext.getCmp('pendingFilesTree').getLoader().load(Ext.getCmp('pendingFilesTree').getRootNode());
};

MA.Files = {
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
       tbar: {
           items: [
               { xtype:'tbtext', text:'checkmarks indicate files that are visible to clients' }
           ]
       },
       items: [
               {
               xtype:'treepanel',
               border: false,
               autoScroll: true,
               id:'filesTree',
               animate: true,
               region:'center',
               enableDrop:true,
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
               selModel: new Ext.tree.DefaultSelectionModel(
                   { listeners:
                       {
                           selectionchange: function(sm, node) {
                               if (node != null && node.isLeaf()) {
                                   window.location = wsBaseUrl + 'downloadFile?file=' + node.id + '&experiment_id=' + MA.CurrentExperimentId();
                               }
                           }
                       }
                   }),
               //tbar: [{
//                      text: 'add files',
//                      cls: 'x-btn-text-icon',
//                      icon:'static/repo/images/add.png',
//                      handler : function(){
////                      userStore.add(new Ext.data.Record({'user':'', 'type':'1', 'additional_info':''}));
//                      }
//                      }
//                      ],
               listeners:{
                    render: function() {
                        Ext.getCmp('filesTree').getLoader().on("beforeload", function(treeLoader, node) {
                            treeLoader.baseParams.experiment = MA.CurrentExperimentId();
                            }, this);
                        Ext.getCmp('filesTree').getRootNode().expand();
                    },
                   nodedrop: function(de) {
                        Ext.Ajax.request({
                                         method:'GET',
                                    url: wsBaseUrl + 'moveFile',
                                         success: function() { Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
                                         Ext.getCmp('filesTree').getRootNode().expand(); },
                                         failure: function() { Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
                                         Ext.getCmp('filesTree').getRootNode().expand(); },
                                    headers: {
    //                                'my-header': 'foo'
                                    },
                                         params: { file: de.dropNode.id, target: de.target.id, experiment_id: MA.CurrentExperimentId() }
                                    });
                   },
                   checkchange: function(node, checked){
                                   Ext.Ajax.request({
                                       method:'POST',
                                       url: wsBaseUrl + 'shareFile',
                                       success: function() {  },
                                       failure: function() {  },
                                       params: { file: node.id, checked: checked, experiment_id: MA.CurrentExperimentId() }
                                                                   });
                               }
                }
               },
               
               {
               layout:'border',
               region:'east',
               split:true,
               width:200,
//               collapsible:true,
               titleCollapse:false,
               
               items: [
                   {
                   xtype:'treepanel',
                   //bodyStyle:'padding:0px;background:transparent;',
                   autoScroll: true,
                   
                   id:'pendingFilesTree',
                   enableDrag: true,
                   region:'center',
                   title:'pending files',
                   
                       tbar: [{
                             text: 'refresh',
                             handler : function(){
                                  //reload the pending files tree
                                  Ext.getCmp('pendingFilesTree').getLoader().load(Ext.getCmp('pendingFilesTree').getRootNode());
                                  Ext.getCmp('pendingFilesTree').getRootNode().expand();
                             }
                             }
                            ],
                       
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
                       //console.log(de);
                   }
                   }
                   },
                       
                   {
                       xtype:'form',
                       height:120,
                       bodyStyle:'background:transparent;padding:4px;padding-top:15px;',
                       id:'pendingFileUpload',
                       fileUpload:true,
                       region:'south',
                       method:'POST',
                       title:'upload',
                       url:wsBaseUrl + 'uploadFile',
                       items: [
                               {
                               hideLabel:true,
                               xtype: 'fileuploadfield',
                               id: 'quo-attach',
                               emptyText: '',
                               fieldLabel: 'file',
                               name: 'attachfile'
                               }
                           ],
                       buttons: [
                                 {
                                 text: 'Upload',
                                 id:'upload file',
                                 handler: function(){
                                 Ext.getCmp('pendingFileUpload').getForm().submit(
                                                                                   {   successProperty: 'success',        
                                                                                   success: function (form, action) {
                                                                                   if (action.result.success === true) {
                                                                                   form.reset(); 
                                                                                   
                                                                                  //reload the pending files tree
                                                                                  Ext.getCmp('pendingFilesTree').getLoader().load(Ext.getCmp('pendingFilesTree').getRootNode());
                                                                                   Ext.getCmp('pendingFilesTree').getRootNode().expand();
                                                                                   
                                                                                   } 
                                                                                   },
                                                                                   failure: function (form, action) {
                                                                                   //do nothing special. this gets called on validation failures and server errors
                                                                                   alert('error submitting form\n' + action.response );
                                                                                   }
                                                                                   });
                                 }
                                 }
                       ]
                   }
               ]
               }
               ]
       }
       ]
};
