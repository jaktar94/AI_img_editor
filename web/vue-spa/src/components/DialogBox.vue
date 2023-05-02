<template>
  <transition name="modal-fade">>
    <div class="modal-backdrop">
      <div class="modal">
        <div class="modal-body">
          {{ msg }}
        </div>

        <div class="modal-footer">
          <template v-if='userAction != "help" && userAction != "uploadPage" && userAction != "uploadPhoto" && userAction != "neuralPhoto"
            && userAction != "acceptError" && userAction != "downloadUnsaved"'>
            <button
                  type="button"
                  class="btn-green yes"
                  @click="submit()"
                >
                  Да
            </button>
            <button
                  type="button"
                  class="btn-green no"
                  @click="cancel()"
                >
                  Нет
            </button>
          </template>
          <template v-else>
            <button
                  type="button"
                  class="btn-green ok"
                  @click="cancel()"
                >
                  Понятно
            </button>
          </template>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'modal',
  props: ['msg', 'userAction'],
  methods: {
    cancel () {
      this.$emit('close')
    },
    submit () {
      this.$emit('accept')
    }
  }
}
</script>

<style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal {
    background: rgba(25, 27, 24, 0.94);
    display: flex;
    flex-direction: column;
    width: 300px;
    padding: 20px 40px;
  }
  .modal-footer {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  .modal-body {
    padding-bottom: 30px;
    width: auto;
    text-align: start;
  }
  .btn-green {
    color: white;
    background: #31A265;
    border: 1px solid #31A265;
    border-radius: 2px;
    width: 70px;
    padding: 7px 9px;
    cursor: pointer;
  }
  .btn-green:hover{
    background: #39c57a;
  }
  .btn-green:active{
    background-color: #82fdbbbd;
    box-shadow: inset 0 0 5px #247248;
  }
  .modal-fade-enter,
  .modal-fade-leave-active {
    opacity: 0;
  }

  .modal-fade-enter-active,
  .modal-fade-leave-active {
    transition: opacity .5s ease
  }
</style>
