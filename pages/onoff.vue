<template>
  <v-container>
    <div class="wrapper_page">
      <h1>สถานะไฟฟ้า</h1>
      <v-row
        class="warpper-input mt-10 drop-shadow2 card"
        v-for="(item, i) in items"
        :key="i"
      >
        <b style="padding: 0px 20px">ช่องที่ {{ i + 1 }}</b>
        <v-switch color="success" v-model="item.status" inset @change="onChange(item)"></v-switch>  
        <!--v-switch ประกาศ@change="onChange(ตัวแปรที่จะเรียกใช้ในฟังก์ชัน  methods onchang) -->
        <v-btn elevation="2" fab :class="item.status ? 'btn-on' : 'btn-off'"
          ><v-icon dark
            >{{ status ? "mdi-lightbulb-on" : "mdi-lightbulb" }}
          </v-icon></v-btn
        >
      </v-row>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      status: true,
      items: [
        { id: 1, status: false },
        { id: 2, status: false },
        { id: 3, status: false },
        { id: 4, status: false },
      ],
    };
  },
  methods:{
  
    onChange(value) {
      if (value.status == true ){
          console.log("ON_"+value.id);
          axios.post('http://127.0.0.1:4003/onDoor', {
            cmd: "ON_"+value.id
          });
      }
      else{
          console.log("OFF_"+value.id);
          axios.post('http://127.0.0.1:4003/onDoor', {
            cmd: "OFF_"+value.id
          });
      } 
    
    }
    
  }

  
};
</script>

<style lang="scss" scoped>
.wrapper_page {
  flex-direction: column;
  align-content: center;

  .warpper-input {
    align-items: center;
    padding: 10px 20px;
    background: #fff;
    border-radius: 15px;
    font-size: 25px;
    justify-content: space-around;
    b {
      margin: 0;
      // color: #fff;
    }

    .btn-on {
      color: #fff;
      background-color: rgb(27, 184, 27) !important;
    }

    .btn-off {
      color: #000;
      background-color: rgba(204, 204, 1) !important;
    }
  }
}
</style>