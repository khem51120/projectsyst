<template>
  <v-container>
    <div class="wrapper_page">
      <h1 class="mb-10">ข้อมูลการตั้งค่า</h1>
      <div
        v-for="item, i in items"
        :key="i"
        class="warpper-input card mt-2"
      >
        <v-col cols="8" style="text-align: left; line-height: 35px">
             
          <h1>{{item.time_start}}</h1>
          <h1>{{ item.time_end }}</h1>
          <p>การเปิด : {{ item.day }}</p>
        </v-col>
        <v-col cols="2">
          <v-switch color="success" v-model="item.status" inset></v-switch>
        </v-col>
        <v-col cols="2">
          <v-btn icon color="red">
            <v-icon size="40">mdi-trash-can</v-icon>
          </v-btn>
        </v-col>
      </div>
      <v-btn
        block
        elevation="2"
        class="my-10"
        color="#526FFF"
        style="color: #fff; border-radius: 15px"
        to="/setting_templatetime"
        ><v-icon size="20">mdi-plus</v-icon>เพิ่ม</v-btn
      >
    </div>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      status: true,
      items: [
        {
          id: 1,
          time_start: "10:20",
          time_end:"13:10",
          day: "อังคาร",
          status: true,
        },
        {
          id: 2,
          time_start: "10:20",
          time_end:"13:50",
          day: "อังคาร",
          status: true,
        },
        {
          id: 3,
          time_start: "10:20",
          time_end:"13:50",
          day: "จันทร์",
          status: true,
        }
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.wrapper_page {
  align-content: center;

  p {
    margin: 0px;
  }

  .warpper-input {
    display: flex;
    flex-direction: row;
    padding: 10px;
    align-items: center;
    border-bottom: 1px solid #c4c4c4;
  }
}
</style>