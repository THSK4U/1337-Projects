/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:50 by Tsellak           #+#    #+#             */
/*   Updated: 2026/07/04 16:05:09 by Tsellak          ###   ########.fr       */
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
	int	i;

	i = 0;
	while (i < dongle->tail)
	{
		if (dongle->queue[i] == coder)
		{
			while (i + 1 < dongle->tail)
			{
				dongle->queue[i] = dongle->queue[i + 1];
				i++;
			}
			dongle->queue[--dongle->tail] = NULL;
			if (dongle->tail > 1
				&& coder->data->scheduler != 0)
				heap_down(dongle);
			return ;
		}
		i++;
	}
}
