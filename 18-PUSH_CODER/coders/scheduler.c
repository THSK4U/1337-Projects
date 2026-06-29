/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:50 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 08:58:50 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	queue_push(t_dongle *dongle, t_coder *coder)
{
	if (dongle->tail >= 2)
		return ;
	dongle->queue[dongle->tail++] = coder;
	if (coder->data->scheduler != 0)
		heap_up(dongle);
}

t_coder	*queue_pop(t_dongle *dongle, t_data *data)
{
	t_coder	*top;

	if (dongle->tail == 0)
		return (NULL);
	top = dongle->queue[0];
	dongle->tail--;
	if (dongle->tail > 0)
		dongle->queue[0] = dongle->queue[dongle->tail];
	dongle->queue[dongle->tail] = NULL;
	if (data->scheduler != 0)
		heap_down(dongle);
	return (top);
}

void	queue_remove(t_dongle *dongle, t_coder *coder)
{
	if (dongle->tail == 0)
		return ;
	if (dongle->queue[0] == coder)
	{
		if (dongle->tail == 2)
			dongle->queue[0] = dongle->queue[1];
		dongle->queue[--dongle->tail] = NULL;
	}
	else if (dongle->queue[1] == coder)
		dongle->queue[--dongle->tail] = NULL;
}
