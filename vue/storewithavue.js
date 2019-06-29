new VTTCue({
    el: '#app',
    data:{
        groupWrapper: "list-group-item",
        isShowingCart:false,
        cart: {
            items: []
        },
    },
    methods:{
        listWrapper:function(){
            this.groupWrapper="list-group-item"
        },
        gridWrapper:function(){
            this.groupWrapper="grid-group-item"
        }
    }
})
