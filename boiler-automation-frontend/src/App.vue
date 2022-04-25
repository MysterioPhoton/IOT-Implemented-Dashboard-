<script setup lang="ts">
import { useDataStore } from "@/store/index";
import { computed, onMounted, ref } from "vue";

const store = useDataStore();

const isDeviceOn = ref(true);
const boxChecked = ref(true);

const data = computed(() => {
  let data = store.data;
  data.sort((a, b) => {
    const a_array: string[] = a.createdAt.split(" ");
    const b_array: string[] = b.createdAt.split(" ");

    const a_date = a_array[0];
    const b_date = b_array[0];

    const dateToDays = (date: string): number => {
      const mm = Number(date.split("/")[0]);
      const dd = Number(date.split("/")[1]);
      const yy = Number(date.split("/")[2]);

      return mm * 30 + dd + yy * 365;
    };

    const a_days = dateToDays(a_date);
    const b_days = dateToDays(b_date);

    if (a_days != b_days) return b_days - a_days;

    const a_time = a_array[1];
    const b_time = b_array[1];

    const timeToSeconds = (time: string): number => {
      const hr = Number(time.split(":")[0]);
      const min = Number(time.split(":")[1]);
      const sec = Number(time.split(":")[2]);

      return hr * 60 * 60 + min * 60 + sec;
    };

    const a_sec = timeToSeconds(a_time);
    const b_sec = timeToSeconds(b_time);

    return b_sec - a_sec;
  });
  return data;
});

onMounted(() => {
  store.fetchData();
});

// setInterval(() => {
//   store.fetchData();
// }, 5000);

const sendDeviceState = async (state: string) => {
  try {
    const res = await fetch("http://localhost:5000/status/" + state);

    const json = await res.json();

    if (json.state == "on") isDeviceOn.value = true;
    else isDeviceOn.value = false;
  } catch (e) {
    console.error("sendDeviceState error", e);
  }
};

const changeDeviceState = async () => {
  if (boxChecked.value) {
    await sendDeviceState("on");
  } else {
    await sendDeviceState("off");
  }

  boxChecked.value = isDeviceOn.value;
};
</script>

<template>
  <section class="head">
    <div class="container">
      <div class="menu">
        <div class="home">
          <a href="index.html"><img src="images/home.png" alt="Home" /></a>
          <a class="name" href="index.html">IOT Dashboard</a>
        </div>
      </div>
    </div>
  </section>

  <section class="main">
    <div class="content">
      <div class="data">
        <table>
          <tr>
            <th>Date</th>
            <th>Time</th>
            <th>Temperature</th>
          </tr>
          <tr v-for="dp in data" :key="dp.id">
            <td>{{ dp.createdAt.split(" ")[0] }}</td>
            <td>{{ dp.createdAt.split(" ")[1] }}</td>
            <td>{{ dp.value }}°C</td>
          </tr>
        </table>
      </div>
    </div>
  </section>

  <section class="switch">
    <div class="content">
      <div class="box">
        <div class="boiler">
          <p>Boiler</p>
          <div class="form-group1">
            <div class="onoff">
              <input
                id="box"
                type="checkbox"
                v-model="boxChecked"
                @change="changeDeviceState"
              />
              <label for="box">
                <span v-if="isDeviceOn">On</span>
                <span v-else>Off</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
