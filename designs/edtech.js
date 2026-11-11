window.initEdtech = ({deadline, left, total, questions}) => {
  const exit = document.querySelector('#ed-exit');
  const start = document.querySelector('#start');
  const play = document.querySelector('#play');
  const action = document.querySelector('#open-grant-dialog');
  const progress = document.querySelector('.ed-availability progress');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let step = -1;
  let exitShown = false;
  let previousFocus;

  document.querySelector('[data-ed-left]').textContent = left;
  document.querySelector('[data-ed-total]').textContent = total;
  progress.max = total;
  progress.value = left;

  const updateTimer = () => {
    const seconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
    const values = [Math.floor(seconds / 86400), Math.floor(seconds / 3600) % 24,
      Math.floor(seconds / 60) % 60, seconds % 60];
    document.querySelectorAll('.ed-digits').forEach(digits => {
      digits.querySelectorAll('b').forEach((digit, index) => {
        const next = String(values[index]).padStart(2, '0');
        if (digit.textContent === next) return;
        digit.textContent = next;
        if (!reducedMotion.matches) digit.animate([{opacity: .55, transform: 'translateY(3px)'}, {opacity: 1, transform: 'translateY(0)'}], {duration: 190, easing: 'ease-out'});
      });
      digits.parentElement.setAttribute('aria-label', `До конца акции: ${values[0]} дн., ${values[1]} ч., ${values[2]} мин.`);
    });
    if (!seconds) {
      document.body.removeAttribute('data-black-friday');
      if (exit.open) exit.close('dismiss');
      clearInterval(ticker);
    }
  };
  const ticker = setInterval(updateTimer, 1000);

  document.documentElement.addEventListener('mouseleave', event => {
    if (event.clientY > 8 || exitShown || step >= questions || Date.now() >= deadline ||
        !matchMedia('(hover: hover) and (pointer: fine)').matches || document.querySelector('dialog[open]')) return;
    exitShown = true;
    previousFocus = document.activeElement;
    const remaining = questions - Math.max(0, step);
    exit.querySelector('.ed-exit-copy').textContent =
      `Осталось ответить на ${remaining} из ${questions} вопросов. В конце покажем разбор ответов и форму заявки на грант и курс в подарок. Грантов осталось ${left} из ${total}.`;
    updateTimer();
    exit.showModal();
  });
  exit.addEventListener('click', event => {
    if (event.target === exit) exit.close('dismiss');
  });
  exit.addEventListener('close', () => {
    if (exit.returnValue === 'resume' && step < 0) start.click();
    else if (previousFocus instanceof HTMLElement) previousFocus.focus({preventScroll: true});
  });

  return {
    render(next) {
      step = next;
      updateTimer();
      if (step === questions - 1 && Date.now() < deadline) {
        const message = document.createElement('p');
        message.className = 'ed-finish';
        message.setAttribute('data-campaign', '');
        const title = document.createElement('strong');
        title.textContent = 'Финишная прямая';
        message.append(title, 'Один ответ до разбора и заявки на грант 40 000 ₽ + подарок');
        play.prepend(message);
      }
      if (step === questions) {
        play.querySelector('.result-grid').classList.add('ed-result-reveal');
        action.classList.add('ed-action-reveal');
      }
    },
  };
};
