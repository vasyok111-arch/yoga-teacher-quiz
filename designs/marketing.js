/* Campaign enhancements for the four marketing experiments. No fabricated activity. */
'use strict';
window.QuizMarketing = ({deadline, grantsLeft, grantsTotal}) => {
  const hook = document.querySelector('#quiz-hook');
  const beats = [
    ['01', 'Сначала — ваша цель', 'Выберите, куда хотите двигаться. Затем попробуете себя в роли преподавателя.'],
    ['02', 'Вы выбираете сценарий', 'Новички, опытная группа или онлайн? От выбора зависят ситуации в вашем уроке.'],
    ['03', 'Теперь — то, что вы уже знаете', 'Два коротких вопроса об основах йоги. Отвечайте сами: объяснения увидите в разборе.'],
    ['04', 'Половина пути пройдена', 'Ещё одно понятие из практики — и вы перейдёте к двум ситуациям на занятии.'],
    ['05', 'Представьте: группу ведёте вы', 'Основы позади. Выберите, как поступить на занятии, — следующий вопрос учтёт ваш ответ.'],
    ['06', 'Ещё один ответ — и ваш разбор', 'Увидите правильные ответы и сможете выбрать курс в подарок к обучению.'],
  ];
  let interval;
  const pad = number => String(number).padStart(2, '0');
  const updateTimers = () => {
    const remaining = Math.max(0, deadline - Date.now());
    const seconds = Math.floor(remaining / 1000);
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor(seconds % 86400 / 3600);
    const minutes = Math.floor(seconds % 3600 / 60);
    const label = `${days ? days + 'д ' : ''}${pad(hours)}:${pad(minutes)}:${pad(seconds % 60)}`;
    document.querySelectorAll('[data-countdown]').forEach(timer => {
      timer.textContent = label;
      timer.setAttribute('datetime', `P${days}DT${hours}H${minutes}M${seconds % 60}S`);
      timer.setAttribute('aria-label', `До конца акции: ${days} дней, ${hours} часов, ${minutes} минут`);
    });
    if (remaining === 0) {
      document.body.removeAttribute('data-black-friday');
      clearInterval(interval);
      if (hook.dataset.step === '5') hook.querySelector('.hook-copy').textContent = 'Увидите правильные ответы и сможете узнать условия обучения в Академии.';
    }
  };
  interval = setInterval(updateTimers, 1000);
  updateTimers();
  return {
    render(step, total) {
      hook.hidden = step < 0 || step >= total;
      if (!hook.hidden) {
        const [index, title, copy] = beats[step];
        hook.querySelector('.hook-index').textContent = index;
        hook.querySelector('.hook-title').textContent = title;
        hook.querySelector('.hook-copy').textContent = copy;
        hook.dataset.step = String(step);
        hook.classList.remove('hook-enter');
        void hook.offsetWidth;
        hook.classList.add('hook-enter');
      }
      document.querySelectorAll('.campaign-ribbon').forEach(ribbon => {
        ribbon.querySelector('.grant-remaining').textContent = `${grantsLeft} / ${grantsTotal}`;
        ribbon.setAttribute('aria-label', `Чёрная пятница: грант 40 000 рублей на обучение и курс в подарок. Остаток по условиям акции: ${grantsLeft} из ${grantsTotal}.`);
      });
      updateTimers();
    },
  };
};
