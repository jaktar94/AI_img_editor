it("After uploading photo open editor", () => {
    cy.visit("http://localhost:8080/");
    cy.get('.filters-container__upload').click();
    const fixtureFile = 'file-ok.jpg';
    cy.get('.input-file').attachFile(fixtureFile);
    cy.get('.filters-container').should('be.visible');
    cy.get('.acpt-btn').should('have.class','btn-disabled')
    cy.get('.rst-btn').should('have.class','btn-disabled')
}); //+
it("Clicking C and NN buttons is correct", () => {
  cy.visit("http://localhost:8080/");
  const fixtureFile = 'file-ok.jpg';
  cy.get('.input-file').attachFile(fixtureFile);
  cy.get('.classic-btn').should('have.class','active-btn');
  cy.get('.filters_list__classic').should('be.visible');
  cy.get('.neural-btn').click();
  cy.get('.neural-btn').should('have.class','active-btn');
  cy.get('.filters_list__neural').should('be.visible');
  cy.get('.classic-btn').click();
}); //+
it("Clicking classic filters", () => {
  let text = '';
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Черно-белое');
  });
  cy.get(':nth-child(2) > .filter-item').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Сепия');
  });
  cy.get(':nth-child(3) > .filter-item').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Инвертирование');
  });
  cy.get(':nth-child(4) > .filter-item').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Рисунок');
  });
  cy.get(':nth-child(5) > .filter-item').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Рельеф');
  });
});//+
it("Clicking neural filters", () => {
  cy.get('.neural-btn').click();
  let text = '';
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.effect-text', { timeout: 40000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Starry night');
  });
  cy.get(':nth-child(2) > .filter-item').click();
  cy.get('.effect-text', { timeout: 40000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Feathers');
  });
  cy.get(':nth-child(3) > .filter-item').click();
  cy.get('.effect-text', { timeout: 40000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Mosaic');
  });
  cy.get(':nth-child(4) > .filter-item').click();
  cy.get('.effect-text', { timeout: 40000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Candy');
  });
  cy.get(':nth-child(5) > .filter-item').click();
  cy.get('.effect-text', { timeout: 40000 }).should(($effect_text) => {
    text = $effect_text.text();
    expect(text).to.equal('Эффект: Wave');
  });
  cy.get('.classic-btn').click();
}); //+
it("Clicking button save", () => {
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.acpt-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text).to.equal(' Применить к изображению выбранный эффект? ');
  })
  cy.get('.yes').click();
  cy.get('.acpt-btn').should('have.class','btn-disabled')
  cy.get('.rst-btn').should('have.class','btn-disabled')
}); //+
it("Clicking button reset", () => {
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.rst-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text).to.equal(' Вы действительно хотите сбросить последний примененный эффект? ');
  })
  cy.get('.yes').click();
  cy.get('.acpt-btn').should('have.class','btn-disabled')
  cy.get('.rst-btn').should('have.class','btn-disabled')
}); //+
it("Clicking button help", () => {
  cy.get('.help-button').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text)
    .to
    .equal(' Для редактирования Вашего изображения представлено два типа фильтров: классический (кнопка "C")' +
            ' и нейронные сети (кнопка "NN"). Обратите внимание: применение фильтров может занять некоторое время ');
  })
  cy.get('.ok').click();
  cy.get('.acpt-btn').should('have.class','btn-disabled')
  cy.get('.rst-btn').should('have.class','btn-disabled')
});
it("Clicking button delete", () => {
  cy.get('.dlt-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text)
    .to
    .equal(' Вернуть исходное изображение? ');
  })
  cy.get('.yes').click();
  cy.get('.acpt-btn').should('have.class','btn-disabled')
  cy.get('.rst-btn').should('have.class','btn-disabled')
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    const text = $effect_text.text();
    expect(text).to.equal('Эффект: отсутствует');
  });
});
it("Clicking button download", () => {
  cy.get('.dwld-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text)
    .to
    .equal(' Начать скачивание изображения? Вы сможете продолжить редактирование ');
  })
  cy.get('.yes').click();
  cy.verifyDownload('file.jpg');
  cy.get('.modal').should('not.be.visible');
});
it("Clicking button upload", () => {
  cy.get('.upld-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text)
    .to
    .equal(' Вы действительно хотите загрузить новое изображение? ');
  })
  cy.get('.yes').click();
  cy.get('.modal').should('not.be.visible');
  cy.get('.welcome-container').should('be.visible');
  const fixtureFile = 'file-ok.jpg';
  cy.get('.input-file').attachFile(fixtureFile);
});
it("Clicking filter and return to initial picture", () => {
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.dlt-btn').click();
  cy.get('.yes').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    const text = $effect_text.text();
    expect(text).to.equal('Эффект: отсутствует');
  });
});
it("Download not saved picture", () => {
  cy.get(':nth-child(2) > .filter-item').click();
  cy.get('.dwld-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.yes').click();
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text)
    .to
    .equal(' На данный момент у вас есть несохраненные изменения. Для загрузки изображения сохраните текущий фильтр и вновь нажмите кнопку "Скачать" ');
  })
  cy.get('.ok').click();
  cy.get('.acpt-btn').click();
  cy.get('.yes').click();
  cy.get('.dwld-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.yes').click();
  cy.verifyDownload('file.jpg');
});
it(" Trying to click classic filter then click neural filter ", () => {
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.effect-text', { timeout: 20000 }).should(($effect_text) => {
    const text = $effect_text.text();
    expect(text).to.equal('Эффект: Черно-белое');
  });
  cy.get('.neural-btn').click();
  cy.get(':nth-child(1) > .filter-item').click();
  cy.get('.effect-text', { timeout: 40000 }).should(($effect_text) => {
    const text = $effect_text.text();
    expect(text).to.equal('Эффект: Starry night');
  });
});
it(" Trying to click neural filter when uploaded img with unsuitable picture ", () => {
  cy.visit("http://localhost:8080/");
  cy.get('.filters-container__upload').click();
  const fixtureFile = 'file.jpg';
  cy.get('.input-file').attachFile(fixtureFile);
  cy.get('.neural-btn').click();
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text).to.equal(' Обратите внимание: фотография с разрешением 960x710 не поддерживает нейронные фильтры.Для применения нейронных фильтров загрузите фотографию меньшего разрешения (не более 800х450) ');
  })
  cy.get('.ok').click();
  cy.get('.filters_list__classic').should('be.visible');
  cy.get('.neural-btn').should('not.have.class','active-btn');

});
it(" Trying to upload img with incorrect resolution ", () => {
  cy.visit("http://localhost:8080/");
  cy.get('.filters-container__upload').click();
  const fixtureFile = 'file-not.jpg';
  cy.get('.input-file').attachFile(fixtureFile);
  cy.get('.modal').should('be.visible');
  cy.get('.modal-body').should(($modal_text) => {
    const text = $modal_text.text();
    expect(text).to.equal(' Фотография с разрешением 1920x100 не поддерживается. Загрузите другую фотографию в рамках ограничений: от 20x20 до 1920х1080 и соотношением сторон не более чем 2 к 1 ');
  })
  cy.get('.ok').click();
  cy.get('.modal').should('not.be.visible');
  cy.get('.welcome-container').should('be.visible');
});
